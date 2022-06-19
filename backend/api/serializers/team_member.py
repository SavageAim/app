"""
Serializers for the Team Member model
"""
# lib
from rest_framework import serializers
# local
from api.models import BISList, Character, TeamMember
from .bis_list import BISListSerializer
from .character import CharacterCollectionSerializer
from .team_member_permissions import TeamMemberPermissionsSerializer

__all__ = [
    'TeamMemberSerializer',
    'TeamMemberModifySerializer',
]


class TeamMemberSerializer(serializers.ModelSerializer):
    bis_list = BISListSerializer()
    character = CharacterCollectionSerializer()
    name = serializers.CharField(source='character.display_name')
    permissions = TeamMemberPermissionsSerializer()

    class Meta:
        model = TeamMember
        exclude = ['team']


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
            Character.objects.get(pk=character_id, user=self.context['user'], verified=True)
        except Character.DoesNotExist:
            raise serializers.ValidationError('Please select a valid, verified Character that you own.')

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
