import auto_prefetch
from django.contrib.postgres.fields import ArrayField
from django.db import models


class Tier(auto_prefetch.Model):
    fights = ArrayField(models.TextField(), default=list)
    max_item_level = models.IntegerField()
    name = models.TextField(unique=True)
    raid_gear_name = models.TextField()
    tome_gear_name = models.TextField()

    def __str__(self):
        return self.name

    class Meta(auto_prefetch.Model.Meta):
        ordering = ['-max_item_level']
