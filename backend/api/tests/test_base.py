from random import choice
from string import ascii_letters
from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from api.models.settings import Settings

__all__ = [
    'SavageAimTestCase',
]


class SavageAimTestCase(APITestCase):
    """
    Superclass with helpful methods
    """

    def _get_user(self):
        """
        Get a user object to auth against the API
        """
        if User.objects.exists():
            return User.objects.first()
        user = User.objects.create_user('test', 'test')
        Settings.objects.create(user=user)
        return user

    def _create_user(self):
        """
        Create an arbitrary user for other purposes than above function
        """
        string = ''.join(choice(ascii_letters) for _ in range(8))
        user = User.objects.create_user(string, string)
        Settings.objects.create(user=user)
        return user
