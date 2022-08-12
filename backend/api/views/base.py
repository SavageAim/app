from typing import Any, Dict, Optional
# lib
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from rest_framework.request import Request
from rest_framework.views import APIView as RFView
# local
from api.errors import InvalidMemberPermissionsError
from api.models import Team, TeamMember

CHANNEL_LAYER = get_channel_layer()


class APIView(RFView):
    """
    Base class for all views with extra handling built in
    """

    def _get_team_as_leader(self, request: Request, team_id: str) -> Optional[Team]:
        """
        Given a team id, check if the request to use a Team Leader restricted API method is valid
        """
        try:
            team = Team.objects.get(pk=team_id)
        except (Team.DoesNotExist, ValidationError):
            return None

        # Check Team Member permissions
        try:
            # Handling multiple members per character
            members = team.members.filter(character__user=request.user)
            valid = False
            for member in members:
                if member.lead:
                    valid = True
                    break

            if not valid:
                raise InvalidMemberPermissionsError()
        except (TeamMember.DoesNotExist, InvalidMemberPermissionsError):
            return None

        return team

    def _get_team_with_permission(self, request: Request, team_id: str, permission: str) -> Optional[Team]:
        """
        Given a Team ID, check if the request to use a restricted command is allowed
        Check against the given permission name to determine this fact
        Return the Team object if found, otherwise return None
        """
        try:
            team = Team.objects.get(pk=team_id)
        except (Team.DoesNotExist, ValidationError):
            return None

        # Check Team Member permissions
        try:
            # Handling multiple members per character
            members = team.members.filter(character__user=request.user)
            valid = False
            for member in members:
                if member.has_permission(permission):
                    valid = True
                    break

            if not valid:
                raise InvalidMemberPermissionsError()
        except (TeamMember.DoesNotExist, InvalidMemberPermissionsError):
            return None

        return team

    def _send_to_user(self, user: Optional[User], event: Dict[str, Any]):
        if user is None:
            return

        if CHANNEL_LAYER is not None:
            async_to_sync(CHANNEL_LAYER.group_send)(f'user-updates-{user.id}', event)

    def _send_to_team(self, team: Team, event: Dict[str, Any]):
        if CHANNEL_LAYER is not None:
            async_to_sync(CHANNEL_LAYER.group_send)(f'team-updates-{team.id}', event)
