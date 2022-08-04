"""
Serializers for the Team models
"""
# lib
from rest_framework import serializers
# local
from api.models import BISList, Character, Team, TeamMember, Tier
from .team_member import TeamMemberSerializer
from .tier import TierSerializer

__all__ = [
    'TeamSerializer',
    'TeamCreateSerializer',
    'TeamUpdateSerializer',
]


class TeamSerializer(serializers.ModelSerializer):
    members = TeamMemberSerializer(many=True)
    tier = TierSerializer()

    class Meta:
        model = Team
        fields = '__all__'


class TeamUpdateSerializer(serializers.ModelSerializer):
    team_lead = serializers.IntegerField()
    tier_id = serializers.IntegerField()

    class Meta:
        model = Team
        fields = ['name', 'tier_id', 'team_lead']
        write_only_fields = ['team_lead']

    def validate_tier_id(self, tier_id: int) -> int:
        """
        Ensure that the Tier id value sent is valid integer, and refers to a valid Tier object
        """
        # Ensure it corresponds with a member of this team
        try:
            Tier.objects.get(pk=tier_id)
        except Tier.DoesNotExist:
            raise serializers.ValidationError('Please select a valid Tier.')

        return tier_id

    def validate_team_lead(self, team_lead_id: int) -> int:
        """
        Ensure that the team lead id is a valid int and refers to a valid member of the team.
        The sent team lead id will be the id of the character, the returned value the id of the TM object.
        """
        # Ensure it corresponds with a member of this team
        try:
            member = self.instance.members.filter(character__user__isnull=False).get(character__pk=team_lead_id)
        except TeamMember.DoesNotExist:
            raise serializers.ValidationError('Please select a non-proxy Member of the Team to be the new team lead.')

        return member.id


class TeamCreateSerializer(serializers.ModelSerializer):
    bis_list_id = serializers.IntegerField()
    character_id = serializers.IntegerField()
    tier_id = serializers.IntegerField()

    class Meta:
        model = Team
        fields = ['character_id', 'bis_list_id', 'name', 'tier_id']

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

    def validate_tier_id(self, tier_id: int) -> int:
        """
        Ensure that the Tier id value sent is valid integer, and refers to a valid Tier object
        """
        # Ensure it corresponds with a member of this team
        try:
            Tier.objects.get(pk=tier_id)
        except Tier.DoesNotExist:
            raise serializers.ValidationError('Please select a valid Tier.')

        return tier_id

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
