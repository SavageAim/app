"""
Model for managing the Teams in the system
"""
# stdlib
import string
import uuid
from random import choice
# lib
from django.db import models

CHARS = string.ascii_letters + string.digits
CODE_LEN = 32


class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    invite_code = models.CharField(max_length=CODE_LEN)
    name = models.CharField(max_length=64)
    tier = models.ForeignKey('Tier', on_delete=models.CASCADE)

    def __str__(self):
        return f'Team {self.name} @ {self.tier.name}'

    @staticmethod
    def generate_invite_code() -> str:
        """
        Generate a new invite code for a team
        Can be used to regenerate the code later as needed
        """
        code = ''.join(choice(CHARS) for _ in range(CODE_LEN))
        while Team.objects.filter(invite_code=code).exists():
            code = ''.join(choice(CHARS) for _ in range(CODE_LEN))

        return code
