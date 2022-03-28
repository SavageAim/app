import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import User


class UpdatesConsumer(WebsocketConsumer):
    room_group_name: str
    user: User

    def connect(self):
        self.user = self.scope['user']
        self.room_group_name = f'user-updates-{self.user.id}'
        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)

    def notification(self, event):
        """
        Send a notification update request to the socket
        """
        print('sending notification payload')
        payload = {
            'type': 'notification',
            'reloadUrls': ['/notifications/'],
        }
        self.send(text_data=json.dumps(payload))
