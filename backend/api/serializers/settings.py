"""
Serializer for a request user's information
"""
# stdlib
from typing import Dict
# lib
from rest_framework import serializers
# local
from api.models import Settings

__all__ = [
    'SettingsSerializer',
]

NOTIFICATION_VALUES = {True, False}


class SettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Settings
        fields = ['loot_manager_version', 'notifications', 'theme']

    def validate_notifications(self, notifications: Dict[str, bool]) -> Dict[str, bool]:
        """
        Ensure that the notifications dict sent by the user only contains valid keys
        """
        for key, value in notifications.items():
            # Check that the key is in the allowed strings, and the value is a valid bool
            if key not in Settings.NOTIFICATIONS:
                raise serializers.ValidationError(f'"{key}" is not a valid choice.')
            if value not in NOTIFICATION_VALUES:
                raise serializers.ValidationError(f'"{key}" does not have a boolean for a value.')
        return notifications
