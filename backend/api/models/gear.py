"""
Model for storing the types of Gear in the game

Will be starting with just 6.0 gear
"""
from django.contrib.postgres.fields import ArrayField
from django.db import models


class Gear(models.Model):
    # Arrays of extra names to check / use when importing Gear that has unique names.
    # extra_import_classes are checked with Levenstein distance.
    extra_import_classes = ArrayField(models.CharField(max_length=64), default=list)
    # extra_import_names are checked to see if the item is present in the list directly.
    extra_import_names = ArrayField(models.CharField(max_length=128), default=list)

    has_accessories = models.BooleanField(default=False)
    has_armour = models.BooleanField(default=False)
    has_weapon = models.BooleanField(default=False)
    item_level = models.IntegerField()
    name = models.TextField()

    class Meta:
        unique_together = ['name', 'item_level']
        ordering = ['-item_level', '-id']
