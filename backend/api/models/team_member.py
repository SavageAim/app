"""
Link model between Teams, Characters and the List they are currently using
"""
# lib
from django.db import models


class TeamMember(models.Model):
    # Map of permission name to the number to compare against bitwise
    PERMISSION_FLAGS = {
        'loot_manager': 1,
        'proxy_manager': 2,
    }

    bis_list = models.ForeignKey('BISList', on_delete=models.PROTECT)
    character = models.ForeignKey('Character', on_delete=models.CASCADE)
    lead = models.BooleanField(default=False)
    permissions = models.IntegerField(default=0)
    team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='members')

    def __str__(self):
        return f'{self.character.name} ({self.character.world}), member of {self.team.name}.'

    class Meta:
        ordering = ['-bis_list__job__role', 'bis_list__job__ordering']
        unique_together = ['character', 'team']

    def check_permission(self, permission: str) -> bool:
        """
        Given a permission name to check, see if this member has permission for it
        """
        return self.lead or bool(self.permissions & self.PERMISSION_FLAGS.get(permission, 0))
