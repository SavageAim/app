"""
Team Member Views

Basically just a management interface of Team Membership;

- Leave / Kick from Team
- Change character / bis list linking
"""

# lib
from django.core.exceptions import ValidationError
from drf_spectacular.utils import OpenApiResponse
from drf_spectacular.views import extend_schema
from rest_framework.request import Request
from rest_framework.response import Response

# local
from .base import APIView, ImportAPIView
from api.lodestone_scraper import CharacterNotFoundError, LodestoneError, LodestoneScraper, MismatchedJobError
from api.models import Gear, TeamMember
from api.serializers import (
    TeamMemberSerializer,
    TeamMemberModifySerializer,
    TeamMemberPermissionsModifySerializer,
)


class TeamMemberResource(APIView):
    """
    Management of Team Member Objects
    """
    queryset = TeamMember
    serializer_class = TeamMemberSerializer

    @extend_schema(
        tags=['team_member'],
        responses={
            200: TeamMemberSerializer,
            404: OpenApiResponse(description='The Team ID does not exist or the Member ID is not valid.'),
        }
    )
    def get(self, request: Request, team_id: str, pk: id) -> Response:
        """
        Read the Membership data for a Character that the requesting User owns in a given Team.
        """
        try:
            obj = TeamMember.objects.get(pk=pk, team_id=team_id, character__user=request.user)
        except (TeamMember.DoesNotExist, ValidationError):
            return Response(status=404)

        data = TeamMemberSerializer(instance=obj).data
        return Response(data)

    @extend_schema(
        tags=['team_member'],
        request=TeamMemberModifySerializer,
        responses={
            204: OpenApiResponse(description='Membership information updated successfully!'),
            400: OpenApiResponse(description='Sent data is invalid.'),
            404: OpenApiResponse(description='The Team ID does not exist or the Member ID is not valid.'),
        }
    )
    def put(self, request: Request, team_id: str, pk: id) -> Response:
        """
        Update some of the Membership data for a Character that the requesting User owns in a given Team.
        """
        try:
            obj = TeamMember.objects.get(pk=pk, team_id=team_id, character__user=request.user)
        except (TeamMember.DoesNotExist, ValidationError):
            return Response(status=404)

        serializer = TeamMemberModifySerializer(instance=obj, data=request.data, context={'user': request.user, 'team': obj.team})
        serializer.is_valid(raise_exception=True)

        obj.character_id = serializer.validated_data['character_id']
        obj.bis_list_id = serializer.validated_data['bis_list_id']
        obj.save()

        # Websocket stuff
        self._send_to_team(obj.team, {'type': 'team', 'id': str(obj.team.id), 'invite_code': str(obj.team.invite_code)})
        for tm in obj.team.members.all():
            self._send_to_user(tm.character.user, {'type': 'character', 'id': tm.character.pk})

        return Response(status=204)

    @extend_schema(
        tags=['team_member'],
        responses={
            204: OpenApiResponse(description='Membership information deleted successfully!'),
            404: OpenApiResponse(description='The Team ID does not exist or the Member ID is not valid.'),
        }
    )
    def delete(self, request: Request, team_id: str, pk: id) -> Response:
        """
        Delete the Membership record for a Member of a Team.

        This method can be run by two people;
        1. The owner of the Member can run this method to leave the specified Team.
        2. The leader of the Team can run this method to kick the specified Member from the Team.
        """
        try:
            obj = TeamMember.objects.get(pk=pk, team_id=team_id)
        except (TeamMember.DoesNotExist, ValidationError):
            return Response(status=404)

        # Check permissions and kick status - Request is valid if;
        #   - Anyone with the Proxy Manager permission is kicking a proxy
        #   - The Team Leader is kicking someone *else* from the Team.
        #   - Someone themselves is choosing to leave the team.
        kick: bool

        # Branch off between a targeted Proxy Character vs non-Proxy
        if obj.character.user is None:
            # Proxy Character being kicked, check requesting user's permissions
            kick = True
            user_members = obj.team.members.filter(character__user=request.user)
            valid = False
            for member in user_members:
                if member.has_permission('proxy_manager'):
                    valid = True
                    break
            if not valid:
                return Response(status=404)
        else:
            # The character in question is not a Proxy so handle the permissions as before
            if obj.character.user is not None and obj.character.user.id == request.user.id:
                # Non Proxy Character attempting to leave
                kick = False
            elif obj.team.members.get(lead=True).character.user.id == request.user.id:
                # Team Leader making request; valid and is kick request
                kick = True
            else:
                # If anything else, return a 404
                return Response(status=404)

        obj.team.remove_character(obj.character, kick)

        # Websocket stuff
        self._send_to_team(obj.team, {'type': 'team', 'id': str(obj.team.id), 'invite_code': str(obj.team.invite_code)})
        for tm in TeamMember.objects.filter(team_id=team_id).select_related('character', 'character__user'):
            self._send_to_user(tm.character.user, {'type': 'character', 'id': tm.character.pk})

        # Special handling for Proxy characters, we should delete them here
        if obj.character.user is None:
            obj.character.delete()

        return Response(status=204)


class TeamMemberCurrentGearResource(ImportAPIView):
    """
    Allow the Team Lead to force-sync a TeamMember's current gear with their lodestone data.
    """

    @extend_schema(
        tags=['team_member'],
        responses={
            204: OpenApiResponse(description='The Member\'s Current Gear has been updated from Lodestone.'),
            400: OpenApiResponse(description='Something went wrong when trying to update.'),
            404: OpenApiResponse(description='The Team ID does not exist or the Member ID is not valid. Alternatively, the requesting User is not the Team Lead.'),
        }
    )
    def post(self, request: Request, team_id: str, pk: id) -> Response:
        """
        Force updating of a Team Member's Current Gear by the Team Lead.
        """
        # Make sure the user in question is the Team Leader
        team = self._get_team_as_leader(request, team_id)
        if team is None:
            return Response(status=404)

        try:
            # Attempt to get a valid member of the specified Team
            obj = team.members.get(pk=pk)
        except (TeamMember.DoesNotExist, ValidationError):
            return Response(status=404)

        # Run the Lodestone Import stuff for the character
        character_id = obj.character.lodestone_id
        expected_job = obj.bis_list.job.id
        scraper = LodestoneScraper.get_instance()
        try:
            data = scraper.get_current_gear(character_id, expected_job)
        except CharacterNotFoundError:
            return Response({'message': 'Could not find a Character with the given ID.'}, status=404)
        except LodestoneError:
            return Response({'message': 'An error occurred connecting to Lodestone.'}, status=400)
        except MismatchedJobError as e:
            msg = f'Couldn\'t import Gear from Lodestone. Gear was expected to be for "{expected_job}", but "{e.received}" was found.'
            return Response({'message': msg}, status=406)

        # Now do Levenstein things for matching found gear to Gear objects
        filtered_gear = Gear.objects.filter(
            item_level__gte=data['min_il'],
            item_level__lte=data['max_il'],
        ).values('name', 'id', 'extra_import_classes', 'extra_import_names')

        # Loop through each gear slot and fetch the id based off the name
        bis_obj = obj.bis_list
        for slot, item_name in data['gear'].items():
            current_slot_name = f'current_{slot}_id'
            if slot in self.ARMOUR_SLOTS:
                slot_id = self._get_gear_id(filtered_gear.filter(has_armour=True), item_name)
            elif slot in self.ACCESSORY_SLOTS:
                slot_id = self._get_gear_id(filtered_gear.filter(has_accessories=True), item_name)
            else:
                slot_id = self._get_gear_id(filtered_gear.filter(has_weapon=True), item_name)
            if slot_id == -1:
                continue
            setattr(
                bis_obj,
                current_slot_name,
                slot_id,
            )
        bis_obj.save()

        # Websocket stuff
        self._send_to_team(obj.team, {'type': 'team', 'id': str(obj.team.id), 'invite_code': str(obj.team.invite_code)})
        for tm in obj.team.members.all():
            self._send_to_user(tm.character.user, {'type': 'character', 'id': tm.character.pk})

        return Response(status=204)


class TeamMemberPermissionsResource(APIView):
    """
    Allow for the updating of Team Member permissions by the Team Lead
    """

    @extend_schema(
        tags=['team_member'],
        request=TeamMemberPermissionsModifySerializer,
        responses={
            204: OpenApiResponse(description='The Member\'s permissions have been updated successfully!'),
            400: OpenApiResponse(description='Sent data is invalid.'),
            404: OpenApiResponse(description='The Team ID does not exist or the Member ID is not valid. Alternatively, the requesting User is not the Team Lead.'),
        }
    )
    def put(self, request: Request, team_id: str, pk: id) -> Response:
        """
        Update the Permissions that a Member of a Team has.
        This method can only be run by the Team Leader.

        The permissions use a bitflag approach with the following numbers;
        - `loot_manager` = `1`
        - `proxy_manager` = `2`

        Sending a value of `3` gives both permissions.
        """
        # Make sure the user in question is the Team Leader
        team = self._get_team_as_leader(request, team_id)
        if team is None:
            return Response(status=404)

        try:
            # Attempt to get a valid member of the specified Team
            obj = team.members.get(pk=pk)
        except (TeamMember.DoesNotExist, ValidationError):
            return Response(status=404)

        # Silently return for leader since their permissions shouldn't be updated
        if obj.lead:
            return Response(status=204)

        serializer = TeamMemberPermissionsModifySerializer(instance=obj, data=request.data)
        serializer.is_valid(raise_exception=True)

        obj.permissions = serializer.validated_data['permissions']
        obj.save()

        # Websocket stuff
        self._send_to_team(obj.team, {'type': 'team', 'id': str(obj.team.id), 'invite_code': str(obj.team.invite_code)})
        for tm in obj.team.members.all():
            self._send_to_user(tm.character.user, {'type': 'character', 'id': tm.character.pk})

        return Response(status=204)
