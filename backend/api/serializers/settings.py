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


class SettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Settings
        fields = ['theme']
