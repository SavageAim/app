"""
Serializer for Notification entries
"""
# lib
from rest_framework import serializers
# local
from api.models import Notification

__all__ = [
    'NotificationSerializer',
]


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Notification
