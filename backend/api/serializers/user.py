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
    'UserSerializer',
]


class UserSerializer(serializers.Serializer):
    avatar_url = serializers.SerializerMethodField()
    id = serializers.IntegerField()
    notifications = serializers.SerializerMethodField()
    theme = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()

    def get_avatar_url(self, obj) -> str:
        """
        Given a User, get the avatar url, if one exists, or return None if not
        """
        if hasattr(obj, 'socialaccount_set') and obj.socialaccount_set.exists():
            return obj.socialaccount_set.first().get_avatar_url()
        return ''

    def get_notifications(self, obj) -> Dict[str, bool]:
        """
        Populate a full dictionary of notifications, filling defaults in as needed
        """
        defaults = {key: True for key in Settings.NOTIFICATIONS}

        try:
            defaults.update(obj.settings.notifications)
        except (AttributeError, Settings.DoesNotExist):
            # Don't have to do anything here
            pass

        return defaults

    def get_theme(self, obj) -> str:
        """
        Get the theme the user has set. Defaults to beta if there's no settings instance
        """
        try:
            return obj.settings.theme
        except (AttributeError, Settings.DoesNotExist):
            return 'beta'

    def get_username(self, obj) -> str:
        """
        Use the `get_full_name` function to return the username since that actually works...
        """
        try:
            return obj.get_full_name()
        except AttributeError:
            return 'guest'
