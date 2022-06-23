"""
Serializer for TeamMember Permissions

Overwrites the flags with TeamLead status
"""
from typing import List
# lib
from rest_framework import serializers
# local
from api.models import TeamMember, TeamMemberPermissions

__all__ = [
    'TeamMemberPermissionsSerializer',
    'TeamMemberPermissionsUpdateSerializer',
]


class TeamMemberPermissionsSerializer(serializers.ModelSerializer):
    loot_manager = serializers.SerializerMethodField()
    team_characters = serializers.SerializerMethodField()

    class Meta:
        model = TeamMemberPermissions
        fields = ['loot_manager', 'team_characters']

    def get_loot_manager(self, obj: TeamMemberPermissions) -> bool:
        """
        If the Member is leader, return true, otherwise return the value
        """
        if obj.member.lead:
            return True
        return obj.loot_manager

    def get_team_characters(self, obj: TeamMemberPermissions) -> bool:
        """
        If the Member is leader, return true, otherwise return the value
        """
        if obj.member.lead:
            return True
        return obj.team_characters


class TeamMemberPermissionsUpdateSerializer(serializers.Serializer):
    loot_manager = serializers.ListField(child=serializers.IntegerField())
    team_characters = serializers.ListField(child=serializers.IntegerField())

    def validate_loot_manager(self, loot_manager_ids: List[int]) -> List[int]:
        """
        Ensure that the list of IDs are all of Team Members in the Team
        """
        objs = TeamMember.objects.filter(
            pk__in=loot_manager_ids,
            team=self.context['team'],
        )
        if objs.count() != len(loot_manager_ids):
            raise serializers.ValidationError('Please ensure all sent ids are of valid Team Members.')
        return loot_manager_ids

    def validate_team_characters(self, team_characters_ids: List[int]) -> List[int]:
        """
        Ensure that the list of IDs are all of Team Members in the Team
        """
        objs = TeamMember.objects.filter(
            pk__in=team_characters_ids,
            team=self.context['team'],
        )
        if objs.count() != len(loot_manager_ids):
            raise serializers.ValidationError('Please ensure all sent ids are of valid Team Members.')
        return team_characters_ids
