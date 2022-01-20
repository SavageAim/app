"""
Stores Settings data for Users.
Settings currently stored;
    - bis theme
"""
# lib
from django.contrib.auth.models import User
from django.db import models


class Settings(models.Model):
    BETA = 'beta'
    BLUE = 'blue'
    GREEN = 'green'
    PURPLE = 'purple'
    RED = 'red'
    THEMES = (
        (BETA, BETA),
        (BLUE, BLUE),
        (GREEN, GREEN),
        (PURPLE, PURPLE),
        (RED, RED),
    )

    theme = models.CharField(max_length=24, choices=THEMES)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='settings')
