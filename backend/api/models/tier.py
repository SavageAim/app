
from django.db import models


class Tier(models.Model):
    max_item_level = models.IntegerField()
    name = models.TextField(unique=True)
    raid_gear_name = models.TextField()
    tome_gear_name = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-max_item_level']
