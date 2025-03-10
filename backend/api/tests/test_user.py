from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from .test_base import SavageAimTestCase
from api.models import Settings


class User(SavageAimTestCase):
    """
    Test the /me/ endpoint for logged in and anonymous users
    """

    # def tearDown(self):
    #     Token.objects.all().delete()

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
        user = self._get_user_without_settings()
        self.client.force_authenticate(user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['id'], user.id)
        self.assertTrue(response.json()['notifications']['verify_fail'])

        # Add a notification to the settings and check again
        Settings.objects.create(user=user, theme='beta', notifications={'verify_fail': False})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.json()['notifications']['verify_fail'])
        self.assertTrue(response.json()['notifications']['verify_success'])

    def test_update(self):
        """
        Send an update request and ensure the theme is changed
        Do it twice so we hit the DoesNotExist successfully
        """
        url = reverse('api:user')
        user = self._get_user_without_settings()
        self.client.force_authenticate(user)

        data = {'theme': 'blue', 'notifications': {'verify_fail': False}, 'loot_manager_version': 'fight', 'username': 'abcde'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response)
        user.refresh_from_db()
        self.assertEqual(user.settings.loot_manager_version, 'fight')
        self.assertEqual(user.settings.theme, 'blue')
        self.assertFalse(user.settings.notifications['verify_fail'])
        self.assertEqual(user.get_full_name(), data['username'])
        self.assertFalse(user.settings.loot_solver_greed)

        # Run it again to hit the other block
        data = {'theme': 'purple', 'notifications': {'verify_success': True}, 'username': 'abcde', 'loot_solver_greed': True}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertEqual(user.settings.theme, 'purple')
        self.assertFalse(user.settings.notifications['verify_fail'])
        self.assertTrue(user.settings.notifications['verify_success'])
        self.assertTrue('team_lead' not in user.settings.notifications)
        self.assertEqual(user.settings.loot_manager_version, 'fight')  # Ensure hasn't changed
        self.assertTrue(user.settings.loot_solver_greed)

    def test_update_400(self):
        """
        Send an update with an invalid choice for the setting and ensure the response is 400
        """
        url = reverse('api:user')
        user = self._get_user()
        self.client.force_authenticate(user)

        data = {'theme': 'abcde', 'notifications': {'abcde': 'abcde'}, 'loot_manager_version': 'abcde', 'loot_solver_greed': 'abcde'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['username'], ['This field is required.'])
        self.assertEqual(response.json()['notifications'], ['"abcde" is not a valid choice.'])
        self.assertEqual(response.json()['loot_manager_version'], ['"abcde" is not a valid choice.'])
        self.assertEqual(response.json()['loot_solver_greed'], ['Must be a valid boolean.'])

        data['notifications'] = {'team_lead': 'abcde'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['notifications'], ['"team_lead" does not have a boolean for a value.'])

    def test_update_403(self):
        """
        Ensure the put requests fail for unauthenticated requests
        """
        url = reverse('api:user')
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestUserTokenView(SavageAimTestCase):
    """
    Test that creating a Token for a User works.
    Test for a User creating a new Token, and one regenerating their token.
    """

    def test_create_new_token(self):
        """
        Create a User without a Token.
        Send request to generate a Token.
        Read User data, ensure we get a Token back.
        """
        read_url = reverse('api:user')
        token_url = reverse('api:user_token')
        user = self._get_user()
        self.client.force_authenticate(user)

        with self.assertRaises(Token.DoesNotExist):
            user.auth_token

        # Generate a Token
        response = self.client.patch(token_url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Read User, ensure we get a Token back
        response = self.client.get(read_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.json()['token'])

    def test_regenerate_token(self):
        """
        Create a User with an existing Token.
        Send request to re-generate a Token.
        Read User data, ensure we get a NEW Token back.
        """
        read_url = reverse('api:user')
        token_url = reverse('api:user_token')
        user = self._get_user()
        self.client.force_authenticate(user)
        token = Token.objects.create(user=user)

        # Generate a Token
        response = self.client.patch(token_url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Read User, ensure we get a Token back
        response = self.client.get(read_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.json()['token'], token.key)
