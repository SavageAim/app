"""
Team interaction views

Teams have TeamMember objects that are used to define what characters are involved in them.
This links to requesting users, which is how we check permissions
"""

# lib
from django.core.exceptions import ValidationError
from drf_spectacular.utils import inline_serializer, OpenApiResponse, OpenApiParameter
from drf_spectacular.views import extend_schema
from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
# local
from .base import APIView
from api import notifier
from api.models import Team, TeamMember
from api.serializers import (
    TeamSerializer,
    TeamCreateSerializer,
    TeamUpdateSerializer,
    TeamMemberModifySerializer,
)


class TeamCollection(APIView):
    """
    Methods to interact with a list of Teams that the User has a character in.
    Provides list and create methods.
    """
    queryset = Team
    serializer_class = TeamSerializer(many=True)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                'char_id',
                int,
                description='Filter the response to Teams that the specified Character is in.'),
        ],
    )
    def get(self, request: Request) -> Response:
        """
        Return a list of the Teams that the requesting User has Characters in.
        """
        objs = Team.objects.filter(members__character__user=request.user).order_by('name').distinct()

        # Filter to a specific character
        character = request.query_params.get('char_id', None)
        if character is not None:
            try:
                objs = objs.filter(members__character_id=character)
            except ValueError:
                # Just skip trying to filter
                pass

        data = TeamSerializer(objs, many=True).data
        return Response(data)

    @extend_schema(
        request=TeamCreateSerializer,
        responses={
            201: OpenApiResponse(
                response=inline_serializer('CreateResponse', {'id': serializers.UUIDField()}),
                description='The ID of the created Team.',
            ),
            400: OpenApiResponse(
                response=TeamCreateSerializer,
                description='Errors occurred during validation of sent data. The values will all be lists of strings for any keys that are present.',
            ),
        }
    )
    def post(self, request: Request) -> Response:
        """
        Create a new Team.
        """
        # Ensure the data we were sent is valid
        serializer = TeamCreateSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)

        # If we're all valid, we can create the Team and the first team member object
        obj = Team.objects.create(
            invite_code=Team.generate_invite_code(),
            name=serializer.validated_data['name'],
            tier_id=serializer.validated_data['tier_id'],
        )
        # Create the Member now
        TeamMember.objects.create(
            bis_list_id=serializer.validated_data['bis_list_id'],
            character_id=serializer.validated_data['character_id'],
            team=obj,
            lead=True,
        )

        # Websocket stuff
        self._send_to_user(request.user, {'type': 'team', 'id': str(obj.id), 'invite_code': str(obj.invite_code)})

        # With everything created, return the Team ID
        return Response({'id': obj.id}, status=201)


class TeamResource(APIView):
    """
    Handling team specific requests
    """

    @extend_schema(
        responses={
            200: TeamSerializer,
            404: OpenApiResponse(
                description='Team ID is invalid, or the requesting User has no Characters in the Team.',
            ),
        }
    )
    def get(self, request: Request, pk: str) -> Response:
        """
        Read the data of a specified Team.
        The requesting User must have a Character in the Team to be able to read it.
        """
        try:
            obj = Team.objects.filter(members__character__user=request.user).distinct().get(pk=pk)
        except (Team.DoesNotExist, ValidationError):
            return Response(status=404)

        data = TeamSerializer(instance=obj).data
        return Response(data)

    @extend_schema(
        request=TeamUpdateSerializer,
        responses={
            204: OpenApiResponse(description='The Team details have been updated successfully!'),
            400: OpenApiResponse(
                response=TeamUpdateSerializer,
                description='A map of any errors for the provided Character and BIS data. The values will all be lists of strings for any keys that are present.',
            ),
            404: OpenApiResponse(
                description='Team ID is invalid, or the requesting User does not own the leader of the Team.',
            ),
        }
    )
    def put(self, request: Request, pk: str) -> Response:
        """
        Update information about a specified Team.
        The requesting User must own the Character who leads the Team in order to run this method.
        """
        obj = self._get_team_as_leader(request, pk)
        if obj is None:
            return Response(status=404)

        serializer = TeamUpdateSerializer(instance=obj, data=request.data)
        serializer.is_valid(raise_exception=True)

        if serializer.validated_data.get('name', obj.name) != obj.name:
            notifier.team_rename(obj, serializer.validated_data.get('name'))

        # Pop the team lead information from the serializer and save it, then update who the team lead is
        team_lead_id = serializer.validated_data.pop('team_lead')
        serializer.save()

        # Make the chosen Character the new leader
        obj.make_lead(obj.members.get(pk=team_lead_id))

        # Websocket stuff
        self._send_to_team(obj, {'type': 'team', 'id': str(obj.id), 'invite_code': str(obj.invite_code)})
        for tm in obj.members.all():
            self._send_to_user(tm.character.user, {'type': 'character', 'id': tm.character.pk})
        return Response(status=204)

    @extend_schema(
        request=None,
        responses={
            204: OpenApiResponse(description='The `invite_code` was successfully regenerated!'),
            404: OpenApiResponse(
                description='Team ID is invalid, or the requesting User does not own the leader of the Team.',
            ),
        }
    )
    def patch(self, request: Request, pk: str) -> Response:
        """
        Regenerate the Team's `invite_code`.
        The requesting User must own the Character who leads the Team in order to run this method.
        """
        obj = self._get_team_as_leader(request, pk)
        if obj is None:
            return Response(status=404)

        obj.invite_code = Team.generate_invite_code()
        obj.save()
        return Response(status=204)

    @extend_schema(
        request=None,
        responses={
            204: OpenApiResponse(description='The Team was successfully disbanded!'),
            404: OpenApiResponse(
                description='Team ID is invalid, or the requesting User does not own the leader of the Team.',
            ),
        }
    )
    def delete(self, request: Request, pk: str) -> Response:
        """
        Disband a Team.
        The requesting User must own the Character who leads the Team in order to run this method.
        """
        obj = self._get_team_as_leader(request, pk)
        if obj is None:
            return Response(status=404)

        team_id = str(obj.pk)
        members = list(obj.members.filter(character__user__isnull=False))

        obj.disband()

        # Websocket stuff
        self._send_to_team(obj, {'type': 'team', 'id': team_id, 'invite_code': str(obj.invite_code)})
        for tm in members:
            self._send_to_user(tm.character.user, {'type': 'character', 'id': tm.character.pk})
        return Response(status=204)


class TeamInvite(APIView):
    """
    Methods to interact with a team via its invite code.
    Used to check that an invite code is valid, pull information, and add members to a Team
    """

    @extend_schema(
        request=None,
        responses={
            200: OpenApiResponse(description='The supplied `invite_code` is valid!'),
            404: OpenApiResponse(description='The supplied `invite_code` is invalid.'),
        }
    )
    def head(self, request: Request, invite_code: str) -> Response:
        """
        Check that a Team exists using only its `invite_code`.
        Used by the frontend to validate a User's supplied `invite_code` without having to load the whole Team's data.
        """
        try:
            Team.objects.get(invite_code=invite_code)
        except Team.DoesNotExist:
            return Response(status=404)

        return Response(status=200)

    @extend_schema(
        request=None,
        responses={
            200: TeamSerializer,
            404: OpenApiResponse(description='A Team with the given `invite_code` does not exist.'),
        }
    )
    def get(self, request: Request, invite_code: str) -> Response:
        """
        Retrieve the data for a Team whose `invite_code` matches the one that is supplied.
        """
        try:
            obj = Team.objects.get(invite_code=invite_code)
        except Team.DoesNotExist:
            return Response(status=404)

        data = TeamSerializer(obj).data
        return Response(data)

    @extend_schema(
        request=TeamMemberModifySerializer,
        responses={
            201: OpenApiResponse(
                response=inline_serializer('CreateResponse', {'id': serializers.UUIDField()}),
                description='The ID of the created Team Member',
            ),
            400: OpenApiResponse(
                response=TeamMemberModifySerializer,
                description='Errors occurred during validation of sent data. The values will all be lists of strings for any keys that are present.',
            ),
            404: OpenApiResponse(description='A Team with the given `invite_code` does not exist.'),
        }
    )
    def post(self, request: Request, invite_code: str) -> Response:
        """
        Allow a User to accept an invitation to join a Team by choosing a Character and BISList.
        """
        try:
            obj = Team.objects.get(invite_code=invite_code)
        except Team.DoesNotExist:
            return Response(status=404)

        serializer = TeamMemberModifySerializer(data=request.data, context={'team': obj, 'user': request.user})
        serializer.is_valid(raise_exception=True)

        # If we make it here, create a new Team Member object
        tm = TeamMember.objects.create(team=obj, **serializer.validated_data)

        # Notify the Team Lead
        notifier.team_join(tm.character, obj)

        # Websocket stuff
        self._send_to_team(obj, {'type': 'team', 'id': str(obj.id), 'invite_code': str(obj.invite_code)})
        for tm in obj.members.all():
            self._send_to_user(tm.character.user, {'type': 'character', 'id': tm.character.pk})

        # Return the team id to redirect to the page
        return Response({'id': obj.id}, status=201)
