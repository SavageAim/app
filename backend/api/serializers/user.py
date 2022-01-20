"""
Serializer for a request user's information
"""
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
    theme = serializers.SerializerMethodField()
    username = serializers.CharField()

    def get_avatar_url(self, obj) -> str:
        """
        Given a User, get the avatar url, if one exists, or return None if not
        """
        if hasattr(obj, 'socialaccount_set') and obj.socialaccount_set.exists():
            return obj.socialaccount_set.first().get_avatar_url()
        return ''

    def get_theme(self, obj) -> str:
        """
        Get the theme the user has set. Defaults to beta if there's no settings instance
        """
        try:
            return obj.settings.theme
        except (AttributeError, Settings.DoesNotExist):
            return 'beta'
