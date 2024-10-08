from typing import Any, Dict, Optional
# lib
import jellyfish
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


class ImportAPIView(APIView):
    """
    A further subclass that gives access to a function for doing levenstein stuff.
    """

    ARMOUR_SLOTS = {'head', 'body', 'hands', 'legs', 'feet'}
    ACCESSORY_SLOTS = {'earrings', 'necklace', 'bracelet', 'left_ring', 'right_ring'}

    @staticmethod
    def _get_gear_id(gear_selection: Dict[str, str], item_name: Optional[str]) -> str:
        """
        Find the id of the gear piece that matches the name closest.

        If item_name is None, return -1 for the dropdown option.

        Check the extra_import_classes for distance also
        However, if item_name is present in extra_import_names, immediately return the id
        """
        if item_name is None:
            return -1

        diff = float('inf')
        gear_id = None
        for details in gear_selection:
            if item_name in details['extra_import_names']:
                return details['id']

            curr_diff = jellyfish.levenshtein_distance(details['name'], item_name)
            if curr_diff < diff:
                diff = curr_diff
                gear_id = details['id']

            for extra_class in details['extra_import_classes']:
                curr_diff = jellyfish.levenshtein_distance(extra_class, item_name)
                if curr_diff < diff:
                    diff = curr_diff
                    gear_id = details['id']

        return gear_id
