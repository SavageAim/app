"""
Serializers for the Team Member model
"""
from typing import Dict
# lib
from rest_framework import serializers
# local
from api.models import BISList, Character, TeamMember
from .bis_list import BISListSerializer
from .character import CharacterCollectionSerializer

__all__ = [
    'TeamMemberSerializer',
    'TeamMemberModifySerializer',
    'TeamMemberPermissionsModifySerializer',
]


class TeamMemberSerializer(serializers.ModelSerializer):
    bis_list = BISListSerializer()
    character = CharacterCollectionSerializer()
    name = serializers.CharField(source='character.display_name')
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = TeamMember
        exclude = ['team']

    def get_permissions(self, obj: TeamMember) -> Dict[str, bool]:
        """
        Generate a dictionary of permission classes to a flag stating whether or not this character has that permission
        """
        return {
            permission: obj.lead or bool(obj.permissions & flag)
            for permission, flag in TeamMember.PERMISSION_FLAGS.items()
        }


class TeamMemberModifySerializer(serializers.Serializer):
    bis_list_id = serializers.IntegerField()
    character_id = serializers.IntegerField()

    def validate_character_id(self, character_id: int) -> int:
        """
        Ensure that the sent character id is a valid integer, refers to a character the user controls, and
        isn't already in the team (in the context)
        """
        # Ensure it corresponds with a member of this team
        try:
            Character.objects.get(pk=character_id, user=self.context['user'])
        except Character.DoesNotExist:
            raise serializers.ValidationError('Please select a valid Character that you own.')

        # If the Character is already in the team, that's an error
        members = TeamMember.objects.filter(character_id=character_id, team=self.context['team'])
        if self.instance is not None:
            # Ignore the current instance since if we want to just change the bis list we should be allowed
            members = members.exclude(pk=self.instance.pk)

        if members.exists():
            raise serializers.ValidationError('This Character is already a member of the Team.')

        return character_id

    def validate_bis_list_id(self, bis_list_id: int) -> int:
        """
        Ensure that the bis list id sent is a valid integer, and refers to a valid BIS List belonging to the user.
        We will check that the BIS List is linked to the sent character in the validate method
        """
        # Ensure it corresponds with a valid bis list for the requesting user
        try:
            BISList.objects.get(pk=bis_list_id, owner__user=self.context['user'])
        except BISList.DoesNotExist:
            raise serializers.ValidationError('Please select a valid BISList belonging to your Character.')

        return bis_list_id

    def validate(self, data):
        """
        Ensure that the chosen BIS List is associated with the given Character
        """
        try:
            BISList.objects.get(pk=data['bis_list_id'], owner_id=data['character_id'])
        except BISList.DoesNotExist:
            raise serializers.ValidationError({
                'bis_list_id': 'Please select a valid BISList belonging to your Character.',
            })

        return data


class TeamMemberPermissionsModifySerializer(serializers.Serializer):
    permissions = serializers.IntegerField()

    def validate_permissions(self, permissions: int) -> int:
        """
        Ensure that the permissions value is within the allowed range of integers for permissions
        """
        upper_bound = sum(TeamMember.PERMISSION_FLAGS.values())
        if permissions < 0 or permissions > upper_bound:
            raise serializers.ValidationError('Invalid permissions value, this is more than likely a server error.')

        return permissions
