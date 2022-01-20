"""
Serializer for Gear entries
"""
# lib
from rest_framework import serializers
# local
from api.models import Gear

__all__ = [
    'GearSerializer',
]


class GearSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Gear
