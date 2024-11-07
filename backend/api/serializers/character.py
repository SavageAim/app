"""
Serializers for the Character model
"""
# stdlib
from re import compile
from typing import Dict, List, Union
# lib
from drf_spectacular.utils import extend_schema_field, inline_serializer
from rest_framework import serializers
# local
from api.models import Character
from .bis_list import BISListSerializer

__all__ = [
    'CharacterCollectionSerializer',
    'CharacterDetailsSerializer',
]

NEW_WORLD_PATTERN = compile(r'([a-zA-Z]+) \[([a-zA-Z]+)\] \(\)')


class CharacterCollectionSerializer(serializers.ModelSerializer):
    alias = serializers.CharField(allow_blank=True, required=False)
    proxy = serializers.SerializerMethodField()
    user_id = serializers.IntegerField(required=False)
    bis_lists = serializers.SerializerMethodField()

    class Meta:
        model = Character
        exclude = ['created', 'token', 'user']
        read_only_fields = ['proxy', 'user_id', 'verified']

    def get_proxy(self, char: Character) -> bool:
        """
        Return flag stating if the Character is a proxy char or not
        """
        return char.user is None

    @extend_schema_field(
        inline_serializer(
            'CharacterCollectionBISListSummary',
            {'id': serializers.IntegerField(), 'name': serializers.CharField()},
            many=True,
        ),
    )
    def get_bis_lists(self, char: Character) -> List[Dict[str, Union[str, int]]]:
        """
        Return summaries of bis lists
        """
        return [
            {
                'id': bis.id,
                'name': bis.name if bis.name != '' else bis.job.display_name,
            }
            for bis in char.bis_lists.all()
        ]

    def validate_world(self, world: str) -> str:
        """
        Handle the new format for world and DC that seems to be cropping up
        """
        find = NEW_WORLD_PATTERN.findall(world)
        if len(find) == 1:
            world = f'{find[0][0]} ({find[0][1]})'
        return world

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


class CharacterUpdateSerializer(serializers.ModelSerializer):
    """
    Allow only certain fields on Character models to be updated
    """
    alias = serializers.CharField(max_length=64, allow_blank=True)
    avatar_url = serializers.URLField()
    name = serializers.CharField(max_length=60)
    world = serializers.CharField(max_length=60)

    class Meta:
        model = Character
        fields = ['alias', 'avatar_url', 'name', 'world']
