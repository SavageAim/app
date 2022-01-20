"""
Serializers for the Character model
"""
# lib
from rest_framework import serializers
# local
from api.models import Character
from .bis_list import BISListSerializer

__all__ = [
    'CharacterCollectionSerializer',
    'CharacterDetailsSerializer',
]


class CharacterCollectionSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(required=False)

    class Meta:
        model = Character
        exclude = ['created', 'token', 'user']
        read_only_fields = ['user_id', 'verified']

    def validate_lodestone_id(self, id: str) -> str:
        """
        Ensure that a lodestone id is not in use already for a verified character.

        When a character is verified, it will remove all entries with the same lodestone id.
        """
        id = str(id)

        # Just check that it isn't already in use.
        if Character.objects.filter(lodestone_id=id, verified=True).exists():
            raise serializers.ValidationError('A verified character with this Lodestone ID already exists.')

        return id


class CharacterDetailsSerializer(serializers.ModelSerializer):
    """
    Give the full details of a character, including gear sets, teams, etc
    """
    bis_lists = BISListSerializer(many=True)

    class Meta:
        model = Character
        exclude = ['created', 'user']
