from django.urls import reverse
from rest_framework import status
from .test_base import SavageAimTestCase
from ..lodestone_scraper import LodestoneScraper

SCRAPER = LodestoneScraper.get_instance()
CHAR_ID = '22909725'


class EtroImport(SavageAimTestCase):
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
