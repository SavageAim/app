from io import StringIO
from django.core.management import call_command
from django.urls import reverse
from rest_framework import status
from api.models import Gear, Tier, Job
from .test_base import SavageAimTestCase


class LodestoneGearImport(SavageAimTestCase):
    """
    Test the import of gear from Lodestone.
    This is a volatile test suite since I'm using my main account but it's probably for the best.
    """

    def setUp(self):
        """
        Call the Gear seed command to prepopulate the DB
        """
        call_command('seed', stdout=StringIO())

    def tearDown(self):
        Gear.objects.all().delete()
        Tier.objects.all().delete()
        Job.objects.all().delete()

    def test_import(self):
        """
        - Create a mapping of valid data for importing current data from the game
        - Expect a correct import
        """
        url = reverse('api:plugin_import')
        user = self._get_user()
        self.client.force_authenticate(user)

        # Generate a valid data block for importing
        # Expect use of new extra_import fields on Gear
        # Also include an item that isn't in the website DB, ensure it just returns None
        request_data = {
            'mainhand': {'name': 'Dragon\'s Beard Fists', 'item_level': 650},
            'offhand': {'name': 'Hero\'s Shield', 'item_level': 560},
            'head': {'name': 'Allegiance Blinder', 'item_level': 560},
            'body': {'name': 'Augmented Credendum Cuirass of Fending', 'item_level': 660},
            'hands': {'name': 'Ascension Gloves of Fending', 'item_level': 660},
            'legs': {'name': 'Brioso Bottoms', 'item_level': 560},
            'feet': {'name': 'Diadochos Boots of Fending', 'item_level': 640},
            'earrings': {'name': 'Ascension Earrings of Fending', 'item_level': 660},
            'necklace': {'name': 'Ascension Necklace of Fending', 'item_level': 660},
            'bracelet': {'name': 'Augmented Credendum of Fending', 'item_level': 660},
            'right_ring': {'name': 'Ascension Ring of Fending', 'item_level': 660},
            'left_ring': {'name': 'Brand New Ring', 'item_level': 30},
        }

        response = self.client.post(url, request_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)

        content = response.json()
        self.assertEqual(content['mainhand']['name'], 'Credendum')
        self.assertEqual(content['offhand']['name'], 'Endwalker AF')
        self.assertEqual(content['head']['name'], 'Endwalker AF')
        self.assertEqual(content['body']['name'], 'Augmented Credendum')
        self.assertEqual(content['hands']['name'], 'Ascension')
        self.assertEqual(content['legs']['name'], 'Endwalker AF')
        self.assertEqual(content['feet']['name'], 'Diadochos')
        self.assertEqual(content['earrings']['name'], 'Ascension')
        self.assertEqual(content['necklace']['name'], 'Ascension')
        self.assertEqual(content['bracelet']['name'], 'Augmented Credendum')
        self.assertEqual(content['right_ring']['name'], 'Ascension')
        self.assertIsNone(content['left_ring'])

    def test_import_400(self):
        """
        Send invalid data, ensure proper errors are given
        """
        url = reverse('api:plugin_import')
        user = self._get_user()
        self.client.force_authenticate(user)

        # Generate a valid data block for importing
        # Expect use of new extra_import fields on Gear
        # Also include an item that isn't in the website DB, ensure it just returns None
        request_data = {
            'offhand': {'item_level': 560},
            'head': {'name': 'Allegiance Blinder'},
        }

        response = self.client.post(url, request_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.content)
        self.assertEqual(response.json()['mainhand'], ['This field is required.'])
        self.assertEqual(response.json()['offhand']['name'], ['This field is required.'])
        self.assertEqual(response.json()['head']['item_level'], ['This field is required.'])
