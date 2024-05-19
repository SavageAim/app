from django.urls import reverse
from rest_framework import status
from .test_base import SavageAimTestCase
from ..lodestone_scraper import CharacterNotFoundError, LodestoneScraper, MismatchedJobError

SCRAPER = LodestoneScraper.get_instance()
CHAR_ID = '22909725'
ALT_CHAR_ID = '42935425'


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
            'avatar_url': (
                'https://img2.finalfantasyxiv.com/f/ce3cf70bc9048943a57001f987830daa_'
                '7206469080400ed57a5373d0a9c55c59fc0_96x96.jpg'
            ),
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

    def test_get_current_gear(self):
        """
        Test Plan;
            - Run a gear data pull from my alt that I probably won't play anymore
            - Ensure the returned data matches what we expect
        """
        expected_data = {
            'gear': {
                'mainhand': 'Augmented Ironworks Magitek Daggers',
                'offhand': 'Augmented Ironworks Magitek Daggers',
                'head': 'Koga Hatsuburi',
                'body': 'Augmented Ironworks Corselet of Scouting',
                'hands': 'Koga Tekko',
                'legs': 'Augmented Ironworks Brais of Scouting',
                'feet': 'Koga Kyahan',
                'earrings': 'Menphina\'s Earring',
                'necklace': 'Aetherial Brass Gorget',
                'bracelet': 'Dawn Wristguards',
                'right_ring': 'Brand-new Ring',
                'left_ring': 'Weathered Ring',
            },
            'max_il': 430,
            'min_il': 5,
        }
        data = SCRAPER.get_current_gear(ALT_CHAR_ID, 'NIN')
        self.assertDictEqual(data, expected_data)

    def test_current_gear_pull_from_invalid_character(self):
        """
        Test Plan;
            - Attempt to load data for a character that isn't real
            - Ensure the function raises the CharacterNotFoundError exception
        """
        with self.assertRaises(CharacterNotFoundError):
            SCRAPER.get_current_gear('abcde', 'abc')

    def test_current_gear_pull_from_unexpected_job(self):
        """
        Test Plan;
            - Load data from alt character but specify a different job
            - Ensure the function raises the MismatchedJobError exception
        """
        try:
            SCRAPER.get_current_gear(ALT_CHAR_ID, 'MNK')
            self.fail('gear returned was for MNK')
        except MismatchedJobError as e:
            self.assertEqual(e.received, 'ROG NIN')
