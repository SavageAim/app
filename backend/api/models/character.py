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


class CharacterDetailsManager(models.Manager):

    def with_summaries(self):
        return self.prefetch_related('bis_lists', 'bis_lists__job')

    def with_details(self):
        return self.prefetch_related(
            'bis_lists',
            'bis_lists__bis_body',
            'bis_lists__bis_bracelet',
            'bis_lists__bis_earrings',
            'bis_lists__bis_feet',
            'bis_lists__bis_hands',
            'bis_lists__bis_head',
            'bis_lists__bis_left_ring',
            'bis_lists__bis_legs',
            'bis_lists__bis_mainhand',
            'bis_lists__bis_necklace',
            'bis_lists__bis_offhand',
            'bis_lists__bis_right_ring',
            'bis_lists__current_body',
            'bis_lists__current_bracelet',
            'bis_lists__current_earrings',
            'bis_lists__current_feet',
            'bis_lists__current_hands',
            'bis_lists__current_head',
            'bis_lists__current_left_ring',
            'bis_lists__current_legs',
            'bis_lists__current_mainhand',
            'bis_lists__current_necklace',
            'bis_lists__current_offhand',
            'bis_lists__current_right_ring',
            'bis_lists__job',
        )


class Character(models.Model):
    alias = models.CharField(max_length=64, default='')
    avatar_url = models.URLField()
    # This is used to delete unverified characters after 24h (celery stuff)
    created = models.DateTimeField(auto_now_add=True)
    lodestone_id = models.TextField()
    name = models.CharField(max_length=60)
    token = models.CharField(max_length=40)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    verified = models.BooleanField(default=False)
    world = models.CharField(max_length=60)

    objects = CharacterDetailsManager()

    def __str__(self) -> str:
        return self.display_name

    @property
    def display_name(self) -> str:
        """
        Return the display name for the Character, either the name @ world or the alias where possible
        """
        if self.alias != '':
            return self.alias
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
