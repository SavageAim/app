import json
from typing import List
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import User
from api.models import Team


class UpdatesConsumer(WebsocketConsumer):
    team_channel_names: List[str]
    user: User
    user_channel_name: str

    def connect(self):
        self.user = self.scope['user']
        if not self.user.is_authenticated:
            self.accept()
            return
        self.user_channel_name = f'user-updates-{self.user.id}'
        self.team_channel_names = [
            f'team-updates-{team.id}'
            for team in Team.objects.filter(members__character__user=self.user)
        ]
        async_to_sync(self.channel_layer.group_add)(self.user_channel_name, self.channel_name)
        for team in self.team_channel_names:
            async_to_sync(self.channel_layer.group_add)(team, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        if not self.user.is_authenticated:
            return
        async_to_sync(self.channel_layer.group_discard)(self.user_channel_name, self.channel_name)
        for team in self.team_channel_names:
            async_to_sync(self.channel_layer.group_discard)(team, self.channel_name)

    """
    Methods for each model updates
    """

    def bis(self, event):
        """
        Update BIS List information in the pages that need it
        """
        payload = {
            'model': 'bis',
            'reloadUrls': [
                f'/characters/{event["char"]}/',
                f'/characters/{event["char"]}/bis_list/{event["id"]}/',
                '/team/join/',
            ],
        }
        self.send(text_data=json.dumps(payload))

    def character(self, event):
        """
        Update Character details on the pages that need it
        """
        payload = {
            'model': 'character',
            'reloadUrls': [
                f'/characters/{event["id"]}/',
                '/team/join/',
            ],
        }
        self.send(text_data=json.dumps(payload))

    def loot(self, event):
        """
        Update Loot details on the pages that need it
        """
        payload = {
            'model': 'loot',
            'reloadUrls': [f'/team/{event["id"]}/loot/'],
        }
        self.send(text_data=json.dumps(payload))

    def notification(self, event):
        """
        Send a notification update request to the socket
        """
        payload = {
            'model': 'notification',
            'reloadUrls': ['/notifications/'],
        }
        self.send(text_data=json.dumps(payload))

    def settings(self, event):
        """
        Update User settings
        """
        payload = {
            'model': 'settings',
            'reloadUrls': ['/settings/'],
        }
        self.send(text_data=json.dumps(payload))

    def team(self, event):
        """
        Send payload informing person of Team updates
        """
        payload = {
            'model': 'team',
            'reloadUrls': [
                f'/team/{event["id"]}/',
                f'/team/join/{event["invite_code"]}/',
            ],
        }
        self.send(text_data=json.dumps(payload))
