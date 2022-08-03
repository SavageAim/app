"""
Team Member Views

Basically just a management interface of Team Membership;

- Leave / Kick from Team
- Change character / bis list linking
"""

# lib
from django.core.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
# local
from .base import APIView
from api.models import TeamMember
from api.serializers import (
    TeamMemberSerializer,
    TeamMemberModifySerializer,
)


class TeamMemberResource(APIView):
    """
    Management of Team Member Objects
    """

    def get(self, request: Request, team_id: str, pk: id) -> Response:
        """
        Get the Data for a single Team Member record
        """
        try:
            obj = TeamMember.objects.get(pk=pk, team_id=team_id, character__user=request.user)
        except (TeamMember.DoesNotExist, ValidationError):
            return Response(status=404)

        data = TeamMemberSerializer(instance=obj).data
        return Response(data)

    def put(self, request: Request, team_id: str, pk: id) -> Response:
        """
        Update a pre-existing Team Member object, potentially changing both the linked character and bis list
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
        self._send_to_team(obj.team, {'type': 'team', 'id': str(obj.team.id)})
        for tm in obj.team.members.all():
            self._send_to_user(tm.character.user, {'type': 'character', 'id': tm.character.pk})

        return Response(status=204)

    def delete(self, request: Request, team_id: str, pk: id) -> Response:
        """
        Team Members can leave a team
        Team leaders can kick team members
        """
        try:
            obj = TeamMember.objects.get(pk=pk, team_id=team_id)
        except (TeamMember.DoesNotExist, ValidationError):
            return Response(status=404)

        team = obj.team

        # Check permissions and kick status;
        # Character owner is making request; valid and is leave request
        kick: bool
        if obj.character.user is None or obj.character.user.id == request.user.id:
            kick = False
        # Team Leader making request; valid and is kick request
        elif obj.team.members.get(lead=True).character.user.id == request.user.id:
            kick = True
        # If anything else, return a 404
        else:
            return Response(status=404)

        obj.team.remove_character(obj.character, kick)

        # Websocket stuff
        self._send_to_team(team, {'type': 'team', 'id': str(team.id)})
        for tm in team.members.all():
            self._send_to_user(tm.character.user, {'type': 'character', 'id': tm.character.pk})

        # Special handling for Proxy characters, we should delete them here
        if obj.character.user is None:
            obj.character.delete()

        return Response(status=204)
