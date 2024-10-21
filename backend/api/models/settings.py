"""
Stores Settings data for Users.
Settings currently stored;
    - bis theme
    - notification settings
"""
# lib
import auto_prefetch
from django.contrib.auth.models import User
from django.db import models


class Settings(auto_prefetch.Model):
    LOOT_MANAGER_DEFAULT = 'item'
    LOOT_MANAGER_VERSIONS = [
        (LOOT_MANAGER_DEFAULT, LOOT_MANAGER_DEFAULT),
        ('fight', 'fight'),
    ]
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

    loot_manager_version = models.CharField(max_length=10, choices=LOOT_MANAGER_VERSIONS, default=LOOT_MANAGER_DEFAULT)
    loot_solver_greed = models.BooleanField(default=False)
    notifications = models.JSONField(default=dict)
    theme = models.CharField(max_length=24)
    user = auto_prefetch.OneToOneField(User, on_delete=models.CASCADE, related_name='settings')
