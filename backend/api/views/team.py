"""
Team interaction views

Teams have TeamMember objects that are used to define what characters are involved in them.
This links to requesting users, which is how we check permissions
"""

# lib
from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
# local
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

    def get(self, request: Request) -> Response:
        """
        Return a list of teams for the User.
        Returns a list of all teams the User has characters in, which can be filtered further by query params
        """
        objs = Team.objects.filter(members__character__user=request.user).order_by('name')

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

    def post(self, request: Request) -> Response:
        """
        Create a new team, with the data for the team lead team member
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

        # With everything created, return the Team ID
        return Response({'id': obj.id}, status=201)


class TeamResource(APIView):
    """
    Handling team specific requests
    """

    def get(self, request: Request, pk: str) -> Response:
        """
        Read the data of a Team.
        It must be a Team that the requesting user controls a character in, or the request will fail
        """
        try:
            obj = Team.objects.get(pk=pk, members__character__user=request.user)
        except (Team.DoesNotExist, ValidationError):
            return Response(status=404)

        data = TeamSerializer(instance=obj).data
        return Response(data)

    def put(self, request: Request, pk: str) -> Response:
        """
        Update some data about the Team
        This request can only be run by the user whose character is the team lead
        """
        try:
            obj = Team.objects.get(pk=pk, members__character__user=request.user, members__lead=True)
        except (Team.DoesNotExist, ValidationError):
            return Response(status=404)

        serializer = TeamUpdateSerializer(instance=obj, data=request.data)
        serializer.is_valid(raise_exception=True)

        # Pop the team lead information from the serializer and save it, then update who the team lead is
        team_lead_id = serializer.validated_data.pop('team_lead')
        serializer.save()

        # Make the chosen Character the new leader
        obj.make_lead(obj.members.get(pk=team_lead_id))
        return Response(status=204)

    def patch(self, request: Request, pk: str) -> Response:
        """
        Regenerate the Team's token
        """
        try:
            obj = Team.objects.get(pk=pk, members__character__user=request.user, members__lead=True)
        except (Team.DoesNotExist, ValidationError):
            return Response(status=404)

        obj.invite_code = Team.generate_invite_code()
        obj.save()
        return Response(status=204)

class TeamInvite(APIView):
    """
    Methods to interact with a team via its invite code.
    Used to check that an invite code is valid, pull information, and add members to a Team
    """

    def head(self, request: Request, invite_code: str) -> Response:
        """
        Check a Team's existence purely by URL.
        Will be used by the frontend to check invite code validity without loading team data
        """
        try:
            Team.objects.get(invite_code=invite_code)
        except Team.DoesNotExist:
            return Response(status=404)

        return Response(status=200)

    def get(self, request: Request, invite_code: str) -> Response:
        """
        Return a list of teams for the User.
        Returns a list of all teams the User has characters in, which can be filtered further by query params
        """
        try:
            obj = Team.objects.get(invite_code=invite_code)
        except Team.DoesNotExist:
            return Response(status=404)

        data = TeamSerializer(obj).data
        return Response(data)

    def post(self, request: Request, invite_code: str) -> Response:
        """
        Add a new team member to the team via the invite link
        Characters can only be on a team once
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

        # Return the team id to redirect to the page
        return Response({'id': obj.id}, status=201)
