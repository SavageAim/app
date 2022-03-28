from django.urls import path

from . import consumers

__all__ = [
    'ws_routes',
]

ws_routes = [
    path('ws/updates/', consumers.UpdatesConsumer.as_asgi()),
]
