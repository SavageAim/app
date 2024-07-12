WHOLE_SHEET_URL = 'https://xivgear.app/?page=sl|cbf28d78-86f4-4d3a-b92e-c8be8e2f1aa4'


from io import StringIO
from django.core.management import call_command
from django.urls import reverse
from rest_framework import status
from api.models import Gear, Tier, Job
from .test_base import SavageAimTestCase


class XIVGearImportTests(SavageAimTestCase):
    """
    Test that we can import data from XIVGear
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

    def test_import_sheet_url(self):
        """
        Send a request to import a whole sheet, firstly without a query param.
        Ensure that we get a 202, with the correct response.
        Then send set=1 and ensure we import the correct data.
        """
        url = reverse('api:xivgear_import', kwargs={'id': 'cbf28d78-86f4-4d3a-b92e-c8be8e2f1aa4'})
        user = self._get_user()
        self.client.force_authenticate(user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        response_data = response.json()
        expected = [
            {'index': 0, 'name': 'Just Finished The Expac :)'},
            {'index': 1, 'name': 'Farmed a bunch of tomes'},
            {'index': 2, 'name': 'DId The EXs :)'},
        ]
        for index, expected_item in enumerate(expected):
            self.assertDictEqual(response_data[index], expected_item, response_data)

        # Now request a set from the sheet
        url += '?set=1'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected = {
            'name': 'Farmed a bunch of tomes',
            'job_id': 'GNB',
            'mainhand': Gear.objects.get(name='Neo Kingdom').pk,
            'offhand': Gear.objects.get(name='Neo Kingdom').pk,
            'head': Gear.objects.get(name='Neo Kingdom').pk,
            'body': Gear.objects.get(name='Neo Kingdom').pk,
            'hands': Gear.objects.get(name='Neo Kingdom').pk,
            'legs': Gear.objects.get(name='Neo Kingdom').pk,
            'feet': Gear.objects.get(name='Neo Kingdom').pk,
            'earrings': Gear.objects.get(name='Neo Kingdom').pk,
            'necklace': Gear.objects.get(name='Neo Kingdom').pk,
            'bracelet': Gear.objects.get(name='Neo Kingdom').pk,
            'right_ring': Gear.objects.get(name='Neo Kingdom').pk,
            'left_ring': Gear.objects.get(name='Epochal').pk,
            'min_il': 690,
            'max_il': 700,
        }
        self.assertDictEqual(response.json(), expected)

    def test_import_single_set_url(self):
        """
        Send a request that imports a URL that only contains a single set, and ensure that the correct data is returned
        """
        url = reverse('api:xivgear_import', kwargs={'id': '289656d9-dc12-4625-a8ac-4d5c32e444f4'})
        user = self._get_user()
        self.client.force_authenticate(user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Build an expected data packet
        expected = {
            'name': 'DId The EXs :)',
            'job_id': 'GNB',
            'mainhand': Gear.objects.get(name='Skyruin').pk,
            'offhand': Gear.objects.get(name='Skyruin').pk,
            'head': Gear.objects.get(name='Neo Kingdom').pk,
            'body': Gear.objects.get(name='Neo Kingdom').pk,
            'hands': Gear.objects.get(name='Neo Kingdom').pk,
            'legs': Gear.objects.get(name='Neo Kingdom').pk,
            'feet': Gear.objects.get(name='Neo Kingdom').pk,
            'earrings': Gear.objects.get(name='Resilient').pk,
            'necklace': Gear.objects.get(name='Resilient').pk,
            'bracelet': Gear.objects.get(name='Resilient').pk,
            'right_ring': Gear.objects.get(name='Neo Kingdom').pk,
            'left_ring': Gear.objects.get(name='Resilient').pk,
            'min_il': 700,
            'max_il': 710,
        }
        self.assertDictEqual(response.json(), expected)

    def test_import_sheet_with_single_set_url(self):
        """
        Send a request that imports a URL that contains a sheet with only one gearset, and ensure that the correct data is returned
        """
        url = reverse('api:xivgear_import', kwargs={'id': '511f9882-30ac-4d8b-b3c4-391c3659211e'})
        user = self._get_user()
        self.client.force_authenticate(user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Build an expected data packet
        expected = {
            'name': 'Default Set',
            'job_id': 'GNB',
            'mainhand': Gear.objects.get(name='Majestic Manderville').pk,
            'offhand': Gear.objects.get(name='Majestic Manderville').pk,
            'head': Gear.objects.get(name='Diadochos').pk,
            'body': Gear.objects.get(name='Diadochos').pk,
            'hands': Gear.objects.get(name='Diadochos').pk,
            'legs': Gear.objects.get(name='Diadochos').pk,
            'feet': Gear.objects.get(name='Diadochos').pk,
            'earrings': Gear.objects.get(name='Diadochos').pk,
            'necklace': Gear.objects.get(name='Diadochos').pk,
            'bracelet': Gear.objects.get(name='Diadochos').pk,
            'right_ring': Gear.objects.get(name='Diadochos').pk,
            'left_ring': Gear.objects.get(name='Diadochos').pk,
            'min_il': 640,
            'max_il': 645,
        }
        self.assertDictEqual(response.json(), expected)

    def test_import_set_with_relic(self):
        """
        Send a request that imports a URL that contains a set with a relic, to ensure we handle relics correctly
        """
        url = reverse('api:xivgear_import', kwargs={'id': '96f0e9f9-e128-4db4-8e36-d3b81e0eb533'})
        user = self._get_user()
        self.client.force_authenticate(user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Build an expected data packet
        expected = {
            'name': 'Default Set',
            'job_id': 'GNB',
            'mainhand': Gear.objects.get(name='Majestic Manderville').pk,
            'offhand': Gear.objects.get(name='Majestic Manderville').pk,
            'head': Gear.objects.get(name='Diadochos').pk,
            'body': Gear.objects.get(name='Diadochos').pk,
            'hands': Gear.objects.get(name='Diadochos').pk,
            'legs': Gear.objects.get(name='Diadochos').pk,
            'feet': Gear.objects.get(name='Diadochos').pk,
            'earrings': Gear.objects.get(name='Diadochos').pk,
            'necklace': Gear.objects.get(name='Diadochos').pk,
            'bracelet': Gear.objects.get(name='Diadochos').pk,
            'right_ring': Gear.objects.get(name='Diadochos').pk,
            'left_ring': Gear.objects.get(name='Diadochos').pk,
            'min_il': 640,
            'max_il': 645,
        }
        self.assertDictEqual(response.json(), expected)

    def test_import_pld_set(self):
        """
        Send a request that imports a URL that contains a set for a PLD, to ensure we handle offhands correctly
        """
        url = reverse('api:xivgear_import', kwargs={'id': 'b8528957-011e-4af0-84d6-79ad8e24ac91'})
        user = self._get_user()
        self.client.force_authenticate(user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Build an expected data packet
        expected = {
            'name': 'Default Set',
            'job_id': 'PLD',
            'mainhand': Gear.objects.get(name='Neo Kingdom').pk,
            'offhand': Gear.objects.get(name='Skyruin').pk,
            'head': Gear.objects.get(name='Dawntrail Artifact Gear').pk,
            'body': Gear.objects.get(name='Dawntrail Artifact Gear').pk,
            'hands': Gear.objects.get(name='Dawntrail Artifact Gear').pk,
            'legs': Gear.objects.get(name='Dawntrail Artifact Gear').pk,
            'feet': Gear.objects.get(name='Dawntrail Artifact Gear').pk,
            'earrings': Gear.objects.get(name='Epochal').pk,
            'necklace': Gear.objects.get(name='Epochal').pk,
            'bracelet': Gear.objects.get(name='Epochal').pk,
            'right_ring': Gear.objects.get(name='Epochal').pk,
            'left_ring': Gear.objects.get(name='Epochal').pk,
            'min_il': 690,
            'max_il': 710,
        }
        self.assertDictEqual(response.json(), expected)

    def test_import_400(self):
        """
        Send requests that will generate 400 errors for the various cases that cause them.
        - Test with an invalid id (gives a 500 error on their system atm)
        - `set` param is not a number
        - xivapi fails (not sure if i can test this but i have handling for it in place)
        """
        url = reverse('api:xivgear_import', kwargs={'id': 'abcde'})
        user = self._get_user()
        self.client.force_authenticate(user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        url = reverse('api:xivgear_import', kwargs={'id': 'cbf28d78-86f4-4d3a-b92e-c8be8e2f1aa4'})
        response = self.client.get(url + '?set=abcde')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['message'], '`set` query parameter was not a valid number.')
