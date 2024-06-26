from io import StringIO
from django.core.management import call_command
from django.urls import reverse
from rest_framework import status
from api.models import Gear, Tier, Job
from .test_base import SavageAimTestCase


class EtroImport(SavageAimTestCase):
    """
    Test the Etro Import view to ensure it works as we expect

    Currently using https://etro.gg/gearset/48e6d8c0-afd8-4857-a320-70528884ac86 for testing
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
        List Gears from the API, ensure same order as in DB in general
        """
        url = reverse('api:etro_import', kwargs={'id': '48e6d8c0-afd8-4857-a320-70528884ac86'})
        user = self._get_user()
        self.client.force_authenticate(user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Build an expected data packet
        expected = {
            'name': 'BiS DNC ilvl 600 (2.47) - 6.11',
            'job_id': 'DNC',
            'mainhand': Gear.objects.get(name='Ultimate of the Heavens').pk,
            'offhand': Gear.objects.get(name='Ultimate of the Heavens').pk,
            'head': Gear.objects.get(name='Asphodelos', has_armour=True).pk,
            'body': Gear.objects.get(name='Asphodelos', has_armour=True).pk,
            'hands': Gear.objects.get(name='Asphodelos', has_armour=True).pk,
            'earrings': Gear.objects.get(name='Asphodelos', has_armour=True).pk,
            'left_ring': Gear.objects.get(name='Asphodelos', has_armour=True).pk,
            'legs': Gear.objects.get(name='Augmented Radiant Host').pk,
            'feet': Gear.objects.get(name='Augmented Radiant Host').pk,
            'necklace': Gear.objects.get(name='Augmented Radiant Host').pk,
            'bracelet': Gear.objects.get(name='Augmented Radiant Host').pk,
            'right_ring': Gear.objects.get(name='Augmented Radiant Host').pk,
            'min_il': 560,
            'max_il': 605,
        }
        self.assertDictEqual(response.json(), expected)

    def test_import_with_relic(self):
        """
        Test an import of a gearset with a custom relic
        """
        url = reverse('api:etro_import', kwargs={'id': '2745b09f-4023-40e6-93e2-72c652143182'})
        user = self._get_user()
        self.client.force_authenticate(user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Build an expected data packet
        expected = {
            'name': 'test with relic',
            'job_id': 'DRG',
            'mainhand': Gear.objects.get(name='Majestic Manderville').pk,
            'offhand': Gear.objects.get(name='Majestic Manderville').pk,
            'head': Gear.objects.get(name='Ascension', has_armour=True).pk,
            'body': Gear.objects.get(name='Ascension', has_armour=True).pk,
            'hands': Gear.objects.get(name='Ascension', has_armour=True).pk,
            'earrings': Gear.objects.get(name='Ascension', has_armour=True).pk,
            'left_ring': Gear.objects.get(name='Ascension', has_armour=True).pk,
            'legs': Gear.objects.get(name='Ascension', has_accessories=True).pk,
            'feet': Gear.objects.get(name='Ascension', has_accessories=True).pk,
            'necklace': Gear.objects.get(name='Ascension', has_accessories=True).pk,
            'bracelet': Gear.objects.get(name='Ascension', has_accessories=True).pk,
            'right_ring': Gear.objects.get(name='Ascension', has_accessories=True).pk,
            'min_il': 645,
            'max_il': 665,
        }
        self.assertDictEqual(response.json(), expected)

    def test_import_400(self):
        """
        Send a request with an invalid ID, check we get a proper error
        """
        url = reverse('api:etro_import', kwargs={'id': 'abcde'})
        user = self._get_user()
        self.client.force_authenticate(user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
