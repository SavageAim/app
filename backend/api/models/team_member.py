"""
Link model between Teams, Characters and the List they are currently using
"""
# lib
from django.db import models


class TeamMemberManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().select_related(
            'character',
            'character__user',
            'bis_list',
            'bis_list__bis_body',
            'bis_list__bis_bracelet',
            'bis_list__bis_earrings',
            'bis_list__bis_feet',
            'bis_list__bis_hands',
            'bis_list__bis_head',
            'bis_list__bis_left_ring',
            'bis_list__bis_legs',
            'bis_list__bis_mainhand',
            'bis_list__bis_necklace',
            'bis_list__bis_offhand',
            'bis_list__bis_right_ring',
            'bis_list__current_body',
            'bis_list__current_bracelet',
            'bis_list__current_earrings',
            'bis_list__current_feet',
            'bis_list__current_hands',
            'bis_list__current_head',
            'bis_list__current_left_ring',
            'bis_list__current_legs',
            'bis_list__current_mainhand',
            'bis_list__current_necklace',
            'bis_list__current_offhand',
            'bis_list__current_right_ring',
            'bis_list__job',
            'bis_list__owner',
        )


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

    def has_permission(self, permission: str) -> bool:
        """
        Given a permission name to check, see if this member has permission for it
        """
        return self.lead or bool(self.permissions & self.PERMISSION_FLAGS.get(permission, 0))
