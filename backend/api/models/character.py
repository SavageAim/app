"""
Represents an FF character.
Is tied to a User
"""
# stdlib
import string
from random import choice
# lib
from django.contrib.auth.models import User
from django.db import models

CHARACTERS = string.ascii_letters + string.digits
RANDOM_CHARS = 30


class Character(models.Model):
    avatar_url = models.URLField()
    # This is used to delete unverified characters after 24h (celery stuff)
    created = models.DateTimeField(auto_now_add=True)
    lodestone_id = models.TextField()
    name = models.CharField(max_length=60)
    token = models.CharField(max_length=40)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    verified = models.BooleanField(default=False)
    world = models.CharField(max_length=60)

    def __str__(self) -> str:
        return f'{self.name} @ {self.world}'

    @staticmethod
    def generate_token() -> str:
        """
        Generate a token for a Character to use for verification
        """
        code = 'savageaim-' + ''.join(choice(CHARACTERS) for _ in range(RANDOM_CHARS))
        while Character.objects.filter(token=code).exists():
            code = 'savageaim-' + ''.join(choice(CHARACTERS) for _ in range(RANDOM_CHARS))

        return code

    def remove(self):
        """
        Do all the cleanup of a Character's Teams before deleting the Character itself
        """
        for member in self.teammember_set.all():
            member.team.remove_character(self, False)
