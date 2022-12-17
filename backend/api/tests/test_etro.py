from io import StringIO
from django.core.management import call_command
from django.urls import reverse
from rest_framework import status
from api.models import Gear
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
            'min_il': 600,
            'max_il': 605,
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
