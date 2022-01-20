from io import StringIO
from django.core.management import call_command
from django.urls import reverse
from rest_framework import status
from api.models import Tier
from api.serializers import TierSerializer
from .test_base import SavageAimTestCase


class TierCollection(SavageAimTestCase):
    """
    Get a list of Tiers and make sure the correct list is returned
    """

    def setUp(self):
        """
        Call the Tier seed command to prepopulate the DB
        """
        call_command('tier_seed', stdout=StringIO())

    def test_list(self):
        """
        List Tiers from the API, ensure same order as in DB in general
        """
        url = reverse('api:tier_collection')
        user = self._get_user()
        self.client.force_authenticate(user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Get the data locally, ensure it all matches
        local_data = TierSerializer(Tier.objects.all(), many=True).data
        remote_data = response.json()
        for index, item in enumerate(local_data):
            self.assertDictEqual(item, remote_data[index])
