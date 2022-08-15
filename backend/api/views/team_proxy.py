"""
Team Proxy Management Views

This adjusted views give access to the proxy system and allow users to create and edit proxy characters
"""

# lib
from django.core.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
# local
from .base import APIView
from api.models import Character, Team, TeamMember
from api.serializers import (
    BISListModifySerializer,
    CharacterCollectionSerializer,
    TeamSerializer,
    TeamMemberSerializer,
)

PERMISSION_NAME = 'proxy_manager'


class TeamProxyCollection(APIView):
    """
    Handle creation of new Proxy Characters for a Team
    """

    def post(self, request: Request, team_id: str) -> Response:
        """
        Create a new Proxy Character in the specified Team.
        Can currently only be done by the Team Lead.
        """
        team = self._get_team_with_permission(request, team_id, PERMISSION_NAME)
        if team is None:
            return Response(status=404)

        # Check both serializers against the separate parts of the data
        char_data = request.data.get('character', {})
        bis_data = request.data.get('bis', {})

        char_serializer = CharacterCollectionSerializer(data=char_data)
        char_valid = char_serializer.is_valid()

        bis_serializer = BISListModifySerializer(data=bis_data)
        bis_valid = bis_serializer.is_valid()

        if not (char_valid and bis_valid):
            # One or both are invalid, return errors
            return Response({'character': char_serializer.errors, 'bis': bis_serializer.errors}, status=400)

        # Create objects
        char_serializer.save(user_id=None, token=Character.generate_token())
        bis_serializer.save(name='', owner=char_serializer.instance)

        # Add proxy to team
        team.members.create(character=char_serializer.instance, bis_list=bis_serializer.instance)

        # Websocket stuff
        self._send_to_team(team, {'type': 'team', 'id': str(team.id), 'invite_code': str(team.invite_code)})
        for tm in team.members.all():
            self._send_to_user(tm.character.user, {'type': 'character', 'id': tm.character.pk})

        return Response({'id': char_serializer.instance.pk}, status=201)


class TeamProxyResource(APIView):
    """
    Handle a single Proxy Character record (read / update)
    """

    def get(self, request: Request, team_id: str, pk: int) -> Response:
        """
        Read the details of a single Proxy record.
        Can only be performed by a Team Lead
        """
        team = self._get_team_with_permission(request, team_id, PERMISSION_NAME)
        if team is None:
            return Response(status=404)

        try:
            obj = team.members.filter(character__user__isnull=True).distinct().get(character_id=pk)
        except (TeamMember.DoesNotExist, ValidationError):
            return Response(status=404)

        # Return Team, Character and BIS data separately for ease of use
        team_data = TeamSerializer(instance=team).data
        member_data = TeamMemberSerializer(instance=obj).data
        return Response({'team': team_data, 'member': member_data})

    def put(self, request: Request, team_id: str, pk: int) -> Response:
        """
        Update the details of a single Proxy record.
        Can only be performed by a Team Lead.
        Only really updates the BIS List since there's not much need to update anything else.
        """
        team = self._get_team_with_permission(request, team_id, PERMISSION_NAME)
        if team is None:
            return Response(status=404)

        try:
            obj = team.members.filter(character__user__isnull=True).distinct().get(character_id=pk)
        except (TeamMember.DoesNotExist, ValidationError):
            return Response(status=404)

        # Validate the new BIS List data
        serializer = BISListModifySerializer(instance=obj.bis_list, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(name='')

        # Send a WS updates for BIS and Teams
        self._send_to_user(obj.character.user, {'type': 'bis', 'char': obj.character.id, 'id': serializer.instance.pk})
        for tm in team.members.all():
            self._send_to_team(team, {'type': 'team', 'id': str(team.id), 'invite_code': str(team.invite_code)})

        return Response(status=204)


class TeamProxyClaim(APIView):
    """
    A separate view that handles User attempts to claim a Proxy.
    For a little security, the view will expect the invite code to be sent in the data.
    """

    def post(self, request: Request, team_id: str, pk: int) -> Response:
        """
        Make an attempt to claim a Proxy Character
        """
        invite_code = request.data.get('invite_code', '')
        try:
            team = Team.objects.get(pk=team_id, invite_code=invite_code)
        except (Team.DoesNotExist, ValidationError):
            return Response(status=404)

        try:
            obj = team.members.filter(character__user__isnull=True).distinct().get(character_id=pk)
        except (TeamMember.DoesNotExist, ValidationError):
            return Response(status=404)

        # Make a copy of the Proxy Character that belongs to the requesting user
        old_char = obj.character
        new_char = Character.objects.create(
            avatar_url=old_char.avatar_url,
            lodestone_id=old_char.lodestone_id,
            name=old_char.name,
            token=Character.generate_token(),
            user=request.user,
            world=old_char.world,
        )

        # Send the new id back to the requesting user
        return Response({'id': new_char.id}, status=201)
