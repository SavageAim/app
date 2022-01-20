from django.urls import reverse
from rest_framework import status
from .test_base import SavageAimTestCase


class User(SavageAimTestCase):
    """
    Test the /me/ endpoint for logged in and anonymous users
    """

    def test_anonymous_user(self):
        """
        Send a request to /me/ endpoint without logging in.
        Ensure that the id is null
        """
        url = reverse('api:user')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(response.json()['id'])

    def test_authenticated_user(self):
        """
        Send a request to /me/ endpoint as a logged in user.
        Ensure that the id is the same as the user we logged in as
        """
        url = reverse('api:user')
        user = self._get_user()
        self.client.force_authenticate(user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['id'], user.id)

    def test_update(self):
        """
        Send an update request and ensure the theme is changed
        Do it twice so we hit the DoesNotExist successfully
        """
        url = reverse('api:user')
        user = self._get_user()
        self.client.force_authenticate(user)

        data = {'theme': 'blue'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user.refresh_from_db()
        self.assertEqual(user.settings.theme, 'blue')

        # Run it again to hit the other block
        data = {'theme': 'purple'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user.refresh_from_db()
        self.assertEqual(user.settings.theme, 'purple')

    def test_update_400(self):
        """
        Send an update with an invalid choice for the setting and ensure the response is 400
        """
        url = reverse('api:user')
        user = self._get_user()
        self.client.force_authenticate(user)

        data = {'theme': 'abcde'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['theme'], ['"abcde" is not a valid choice.'])

    def test_update_403(self):
        """
        Ensure the put requests fail for unauthenticated requests
        """
        url = reverse('api:user')
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
