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
        Test Plan;
            - Import Eira and ensure her gear matches what I currently had equipped
        """
        url = reverse('api:lodestone_gear_import', kwargs={'character_id': '22909725', 'expected_job': 'GNB'})
        user = self._get_user()
        self.client.force_authenticate(user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.json())

        # Build an expected data packet
        expected = {
            'job_id': 'GNB',
            'mainhand': Gear.objects.get(name='Archeo Kingdom').pk,
            'offhand': Gear.objects.get(name='Archeo Kingdom').pk,
            'head': Gear.objects.get(name='Dark Horse Champion', has_armour=True).pk,
            'body': Gear.objects.get(name='Augmented Quetzalli', has_armour=True).pk,
            'hands': Gear.objects.get(name='Quetzalli', has_armour=True).pk,
            'legs': Gear.objects.get(name='Dark Horse Champion', has_armour=True).pk,
            'feet': Gear.objects.get(name='Augmented Quetzalli', has_armour=True).pk,
            'earrings': Gear.objects.get(name='Dark Horse Champion', has_accessories=True).pk,
            'necklace': Gear.objects.get(name='Dark Horse Champion', has_accessories=True).pk,
            'bracelet': Gear.objects.get(name='Augmented Quetzalli', has_accessories=True).pk,
            'right_ring': Gear.objects.get(name='Augmented Quetzalli', has_accessories=True).pk,
            'left_ring': Gear.objects.get(name='Dark Horse Champion', has_accessories=True).pk,
            'min_il': 710,
            'max_il': 730,
        }
        self.maxDiff = None
        self.assertDictEqual(response.json(), expected)

    def test_import_with_missing_gear(self):
        """
        Test Plan;
            - Create a Job and Gear for starting gear so that the import works out properly.
            - Import a character with missing gear slots, ensure that the API doesn't break.
        """
        Job.objects.create(name='Pugilist', id='PGL', role='dps', ordering=24)
        lalafellin = Gear.objects.create(
            name='Lalafellin',
            item_level=5,
            has_armour=True,
            has_accessories=False,
            has_weapon=False,
        ).pk
        weathered_acc = Gear.objects.create(
            name='Weathered',
            item_level=5,
            has_armour=False,
            has_accessories=True,
            has_weapon=False,
        ).pk
        weathered = Gear.objects.create(
            name='Weathered',
            item_level=1,
            has_armour=False,
            has_accessories=False,
            has_weapon=True,
        ).pk

        url = reverse('api:lodestone_gear_import', kwargs={'character_id': '47800977', 'expected_job': 'PGL'})
        user = self._get_user()
        self.client.force_authenticate(user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.json())

        # Build an expected data packet
        expected = {
            'job_id': 'PGL',
            'mainhand': weathered,
            'offhand': weathered,
            'head': -1,
            'body': lalafellin,
            'hands': lalafellin,
            'legs': lalafellin,
            'feet': lalafellin,
            'earrings': weathered_acc,
            'necklace': weathered_acc,
            'bracelet': weathered_acc,
            'right_ring': -1,
            'left_ring': weathered_acc,
            'min_il': 1,
            'max_il': 5,
        }
        self.maxDiff = None
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
        url = reverse('api:lodestone_gear_import', kwargs={'character_id': '22909725', 'expected_job': 'SAM'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertEqual(
            response.json()['message'],
            'Couldn\'t import Gear from Lodestone. Gear was expected to be for "SAM", but "GNB" was found.',
        )
