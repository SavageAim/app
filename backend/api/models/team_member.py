"""
Link model between Teams, Characters and the List they are currently using
"""
# lib
from django.db import models


class TeamMember(models.Model):
    # TODO - Gotta warn about leaving teams or deleting BISLists (which can't be done yet)
    bis_list = models.ForeignKey('BISList', on_delete=models.PROTECT)
    character = models.ForeignKey('Character', on_delete=models.CASCADE)
    # TODO - Can't delete if you're the raid lead / move raidlead to someone else if character is deleted
    lead = models.BooleanField(default=False)
    team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='members')

    def __str__(self):
        return f'{self.character.name} ({self.character.world}), member of {self.team.name}.'

    class Meta:
        ordering = ['-bis_list__job__role', 'bis_list__job__ordering']
        unique_together = ['character', 'team']
