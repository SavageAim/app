import auto_prefetch
from django.db import models


class XIVVersion(auto_prefetch.Model):
    version = models.TextField(primary_key=True)

    def __str__(self):
        return f'FFXIV Version {self.version}'

    class Meta(auto_prefetch.Model.Meta):
        ordering = ['-version']
