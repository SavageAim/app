from typing import Any, Dict
# lib
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.models import User
from rest_framework.views import APIView as RFView
# local
from api.models import Team

CHANNEL_LAYER = get_channel_layer()


class APIView(RFView):
    """
    Base class for all views with websocket code handling built in
    """

    def _send_to_user(self, user: User, event: Dict[str, Any]):
        if CHANNEL_LAYER is not None:
            async_to_sync(CHANNEL_LAYER.group_send)(f'user-updates-{user.id}', event)

    def _send_to_team(self, team: Team, event: Dict[str, Any]):
        if CHANNEL_LAYER is not None:
            async_to_sync(CHANNEL_LAYER.group_send)(f'team-updates-{team.id}', event)
