"""
Model for managing the game's jobs

Will probably use the job code (PLD etc) as the id, and maintain ordering separately
"""
from django.db import models


class Job(models.Model):
    TANK = 'tank'
    HEAL = 'heal'
    DPS = 'dps'
    ROLES = (
        (TANK, TANK),
        (HEAL, HEAL),
        (DPS, DPS),
    )

    display_name = models.CharField(max_length=64)
    id = models.CharField(max_length=3, primary_key=True, unique=True)
    name = models.CharField(max_length=64)
    ordering = models.IntegerField()  # private field used to manipulate ordering in the lists
    role = models.CharField(max_length=4, choices=ROLES)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-role', 'ordering']
