"""
Serializer for Tier entries
"""
# lib
from rest_framework import serializers
# local
from api.models import Tier

__all__ = [
    'TierSerializer',
]


class TierSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Tier
