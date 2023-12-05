from django.urls import reverse
from rest_framework import status
from .test_base import SavageAimTestCase
from ..lodestone_scraper import CharacterNotFoundError, LodestoneScraper

SCRAPER = LodestoneScraper.get_instance()
CHAR_ID = '22909725'


class LodestoneScraper(SavageAimTestCase):
    """
    Test that the Lodestone Scraper returns what is expected for its various methods
    """

    def test_token_check(self):
        """
        Test Plan;
            - Check my own character profile for a token I know is present.
            - Ensure the scraper function returns None
        """
        err = SCRAPER.check_token(CHAR_ID, 'savageaim')
        self.assertIsNone(err)

    def test_invalid_token_check(self):
        """
        Test Plan;
            - Check my own character profile for a token that is not present.
            - Ensure the scraper function returns the correct error message.
        """
        err = SCRAPER.check_token(CHAR_ID, 'abcdefghijklmnopqrstuvwxyz')
        self.assertEqual(err, 'Could not find the verification code in the Lodestone profile.')

    def test_data_pull(self):
        """
        Test Plan;
            - Load data of my own character, ensure it matches what is expected.
        """
        expected = {
            'avatar_url': 'https://img2.finalfantasyxiv.com/f/ce3cf70bc9048943a57001f987830daa_7206469080400ed57a5373d0a9c55c59fc0_96x96.jpg',
            'name': 'Eira Erikawa',
            'world': 'Lich',
            'dc': 'Light',
        }
        data = SCRAPER.get_character_data(CHAR_ID)
        self.assertDictEqual(data, expected)

        # Also ensure the same data packet is returned from the API version of this function
        self.client.force_login(self._get_user())
        url = reverse('api:lodestone_resource', kwargs={'character_id': CHAR_ID})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        self.assertDictEqual(response.json(), expected)

    def test_data_pull_from_invalid_character(self):
        """
        Test Plan;
            - Attempt to load data for a character that isn't real
            - Ensure the function raises the CharacterNotFoundError exception
        """
        with self.assertRaises(CharacterNotFoundError):
            SCRAPER.get_character_data('abcde')
