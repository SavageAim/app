from io import StringIO
from django.core.management import call_command
from django.urls import reverse
from rest_framework import status
from api.models import Gear
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

    def test_import(self):
        """
        Test Plan;
            - Import Eira and ensure her gear matches what I currently had equipped
        """
        url = reverse('api:lodestone_gear_import', kwargs={'character_id': '22909725', 'expected_job': 'SCH'})
        user = self._get_user()
        self.client.force_authenticate(user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Build an expected data packet
        expected = {
            'job_id': 'SCH',
            'mainhand': Gear.objects.get(name='Mandervillous').pk,
            'offhand': Gear.objects.get(name='Mandervillous').pk,
            'head': Gear.objects.get(name='Ascension', has_armour=True).pk,
            'body': Gear.objects.get(name='Ascension', has_armour=True).pk,
            'hands': Gear.objects.get(name='Augmented Credendum', has_armour=True).pk,
            'legs': Gear.objects.get(name='Augmented Credendum', has_armour=True).pk,
            'feet': Gear.objects.get(name='Ascension', has_armour=True).pk,
            'earrings': Gear.objects.get(name='Augmented Credendum', has_accessories=True).pk,
            'necklace': Gear.objects.get(name='Ascension', has_accessories=True).pk,
            'bracelet': Gear.objects.get(name='Ascension', has_accessories=True).pk,
            'right_ring': Gear.objects.get(name='Augmented Credendum', has_accessories=True).pk,
            'left_ring': Gear.objects.get(name='Credendum', has_accessories=True).pk,
            'min_il': 650,
            'max_il': 665,
        }
        self.assertDictEqual(response.json(), expected)

    def test_import_400_and_404(self):
        """
        Test Plan;
            - Send requests with bad ids and jobs and ensure we get valid responses.
        """
        user = self._get_user()
        self.client.force_authenticate(user)

        # Bad Character ID
        url = reverse('api:lodestone_gear_import', kwargs={'character_id': 'abcde', 'expected_job': 'PLD'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Bad Job ID
        url = reverse('api:lodestone_gear_import', kwargs={'character_id': 'abcde', 'expected_job': 'abcde'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Job ID doesn't match gear
        url = reverse('api:lodestone_gear_import', kwargs={'character_id': '22909725', 'expected_job': 'PLD'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
