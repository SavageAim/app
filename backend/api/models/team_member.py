"""
Link model between Teams, Characters and the List they are currently using
"""
# lib
import auto_prefetch
from django.db import models


class TeamMember(auto_prefetch.Model):
    # Map of permission name to the number to compare against bitwise
    PERMISSION_FLAGS = {
        'loot_manager': 1,
        'proxy_manager': 2,
    }

    bis_list = auto_prefetch.ForeignKey('BISList', on_delete=models.PROTECT)
    character = auto_prefetch.ForeignKey('Character', on_delete=models.CASCADE)
    lead = models.BooleanField(default=False)
    permissions = models.IntegerField(default=0)
    team = auto_prefetch.ForeignKey('Team', on_delete=models.CASCADE, related_name='members')

    def __str__(self):
        return f'{self.character.name} ({self.character.world}), member of {self.team.name}.'

    class Meta(auto_prefetch.Model.Meta):
        ordering = ['-bis_list__job__role', 'bis_list__job__ordering']
        unique_together = ['character', 'team']

    def has_permission(self, permission: str) -> bool:
        """
        Given a permission name to check, see if this member has permission for it
        """
        return self.lead or bool(self.permissions & self.PERMISSION_FLAGS.get(permission, 0))
