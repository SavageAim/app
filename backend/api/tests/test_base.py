from random import choice
from string import ascii_letters
from django.contrib.auth.models import User
from rest_framework.test import APITestCase

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
        return User.objects.create_user('test', 'test')

    def _create_user(self):
        """
        Create an arbitrary user for other purposes than above function
        """
        string = ''.join(choice(ascii_letters) for _ in range(8))
        return User.objects.create_user(string, string)
