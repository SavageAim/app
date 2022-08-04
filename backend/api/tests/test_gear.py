from io import StringIO
from django.core.management import call_command
from django.urls import reverse
from rest_framework import status
from api.models import Gear
from api.serializers import GearSerializer
from .test_base import SavageAimTestCase

MAX_ITEM_LEVEL = 635
MIN_ITEM_LEVEL = 560


class GearCollection(SavageAimTestCase):
    """
    Get a list of Gears and make sure the correct list is returned
    """

    def setUp(self):
        """
        Call the Gear seed command to prepopulate the DB
        """
        call_command('seed', stdout=StringIO())

    def test_list(self):
        """
        List Gears from the API, ensure same order as in DB in general
        """
        url = reverse('api:gear_collection')
        user = self._get_user()
        self.client.force_authenticate(user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Get the data locally, ensure it all matches
        local_data = GearSerializer(Gear.objects.all(), many=True).data
        remote_data = response.json()
        for index, item in enumerate(local_data):
            self.assertDictEqual(item, remote_data[index])

    def test_filters(self):
        """
        Test the API using both filters and ensure correct response is returned
        """
        il_min = 560
        il_max = 570
        url = f'{reverse("api:gear_collection")}?item_level_min={il_min}&item_level_max={il_max}'
        user = self._get_user()
        self.client.force_authenticate(user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # With the specified filters, we should have three Gear types returned; The Last, Endwalker AF, Moonward
        content = response.json()
        self.assertEqual(len(content), 3)
        names = ['Moonward', 'Endwalker AF', 'The Last']
        for index, gear in enumerate(content):
            self.assertTrue(gear['item_level'] in range(il_min, il_max + 1))
            self.assertEqual(gear['name'], names[index])

        # Test invalid filters and ensure we get the whole list back
        url = f'{reverse("api:gear_collection")}?item_level_min=abcde&item_level_max=abcde'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), Gear.objects.count())

    def test_item_levels(self):
        """
        Test that the item levels api endpoint returns appropriate data
        """
        url = reverse('api:item_levels')
        user = self._get_user()
        self.client.force_authenticate(user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        content = response.json()
        # TODO - Change these as needed, hardcoding numbers so I can ensure my logic is right
        self.assertEqual(content['min'], MIN_ITEM_LEVEL)
        self.assertEqual(content['max'], MAX_ITEM_LEVEL)
