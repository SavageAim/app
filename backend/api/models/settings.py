"""
Stores Settings data for Users.
Settings currently stored;
    - bis theme
"""
# lib
from django.contrib.auth.models import User
from django.db import models


class Settings(models.Model):
    theme = models.CharField(max_length=24)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='settings')
