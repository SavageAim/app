"""
Model for storing the types of Gear in the game

Will be starting with just 6.0 gear
"""

from django.db import models


class Gear(models.Model):
    has_accessories = models.BooleanField(default=False)
    has_armour = models.BooleanField(default=False)
    has_weapon = models.BooleanField(default=False)
    item_level = models.IntegerField()
    name = models.TextField()

    class Meta:
        unique_together = ['name', 'item_level']
        ordering = ['-item_level', '-id']
