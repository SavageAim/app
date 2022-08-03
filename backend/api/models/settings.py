"""
Stores Settings data for Users.
Settings currently stored;
    - bis theme
    - notification settings
"""
# lib
from django.contrib.auth.models import User
from django.db import models


class Settings(models.Model):
    NOTIFICATIONS = {
        'loot_tracker_update',
        'team_disband',
        'team_join',
        'team_kick',
        'team_lead',
        'team_leave',
        'team_proxy_claim',
        'team_rename',
        'verify_fail',
        'verify_success',
    }

    notifications = models.JSONField(default=dict)
    theme = models.CharField(max_length=24)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='settings')
