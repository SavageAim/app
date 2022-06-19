"""
Serializer for TeamMember Permissions

Overwrites the flags with TeamLead status
"""
# lib
from rest_framework import serializers
# local
from api.models import TeamMemberPermissions

__all__ = [
    'TeamMemberPermissionsSerializer',
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
