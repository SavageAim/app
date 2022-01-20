"""
Model for tracking loot for a Team

Loot is broken up by the Team (via TeamMember ForeignKey), and Tier that it was received.
Has an obtained date stamp for displaying a timeline of events.
Maintains a flag to indicate if it was need (false (default)) or greed (true)
    If greeded, the api should also send the id of the character's BIS List that should be updated

Whenever loot is tracked, the corresponding slot on the appropriate BIS List
"""
from django.db import models


class Loot(models.Model):
    greed = models.BooleanField(default=False)
    item = models.TextField()
    member = models.ForeignKey('TeamMember', null=True, on_delete=models.SET_NULL)
    obtained = models.DateField()
    team = models.ForeignKey('Team', on_delete=models.CASCADE, null=True)
    tier = models.ForeignKey('Tier', on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.item} obtained by {str(self.member)} on {self.obtained}. Greed: {self.greed}.'

    class Meta:
        ordering = ['-obtained', '-id']
