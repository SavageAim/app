"""
Permissions for Team Members.
"""
# lib
from django.db import models


class TeamMemberPermissions(models.Model):
    """
    Keep track of permissions in boolean fields.
    This is a little more secure than using a JSON field on Member table.
    Being Team Lead will return True for both of these fields.
    """
    # Can the Member use the loot manager to hand out loot
    loot_manager = models.BooleanField(default=False)
    member = models.OneToOneField('TeamMember', on_delete=models.CASCADE, related_name='permissions')
    # Can the Member add or edit Team Characters
    team_characters = models.BooleanField(default=False)
