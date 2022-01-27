"""
Serializer for a request user's information
"""
# lib
from rest_framework import serializers
# local
from api.models import Settings

__all__ = [
    'SettingsSerializer',
]

THEMES = {
    'beta',
    'blue',
    'green',
    'purple',
    'red',
    'trans',
}


class SettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Settings
        fields = ['theme']

    def validate_theme(self, theme: str) -> str:
        """
        Ensure the theme is in the set of allowed themes
        """
        if theme not in THEMES:
            raise serializers.ValidationError(f'"{theme}" is not a valid choice.')
        return theme
