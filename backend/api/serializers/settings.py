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

THEMES = {
    'beta',
    'blue',
    'green',
    'purple',
    'red',
    'traffic',
    'trans',
}


class SettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Settings
        fields = ['notifications', 'theme']

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

    def validate_theme(self, theme: str) -> str:
        """
        Ensure the theme is in the set of allowed themes
        """
        if theme not in THEMES:
            raise serializers.ValidationError(f'"{theme}" is not a valid choice.')
        return theme
