"""
Model for managing the game's jobs

Will probably use the job code (PLD etc) as the id, and maintain ordering separately
"""
import auto_prefetch
from django.db import models


class Job(auto_prefetch.Model):
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

    class Meta(auto_prefetch.Model.Meta):
        ordering = ['-role', 'ordering']

    @classmethod
    def get_in_solver_order(cls):
        return Job.objects.annotate(solver_sort=models.Case(
            models.When(role='dps', then=0),
            models.When(role='tank', then=1),
            default=2,
        )).order_by('solver_sort', 'ordering').all()
