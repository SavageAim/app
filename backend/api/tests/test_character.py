# stdlib
from io import StringIO
from unittest.mock import patch
# lib
from django.core.management import call_command
from django.urls import reverse
from rest_framework import status
# local
from api.models import BISList, Character, Gear, Job
from api.serializers import CharacterCollectionSerializer, CharacterDetailsSerializer
from .test_base import SavageAimTestCase


def _fake_task(pk: int):
    """
    Handle what celery would handle if it were running
    """
    try:
        obj = Character.objects.get(pk=pk, verified=False)
    except Character.DoesNotExist:
        return

    obj.verified = True
    obj.save()


class CharacterCollection(SavageAimTestCase):
    """
    Test the list and create methods
    """

    def tearDown(self):
        """
        Clean up the DB after each test
        """
        Character.objects.all().delete()

    def test_list(self):
        """
        Create a couple of characters for a user and send a list request for them
        ensure the data is returned as expected
        """
        url = reverse('api:character_collection')
        user = self._get_user()
        self.client.force_authenticate(user)

        # Create some users, then send a list request and check the data returned is correct
        char1 = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=user,
            name='Char 1',
            world='Lich',
        )

        char2 = Character.objects.create(
            avatar_url='https://img.savageaim.com/fghij',
            lodestone_id=987654321,
            user=user,
            name='Char 2',
            world='Shiva',
        )

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        content = response.json()
        self.assertEqual(len(content), 2)
        self.assertDictEqual(content[0], CharacterCollectionSerializer(char1).data)
        self.assertDictEqual(content[1], CharacterCollectionSerializer(char2).data)

    def test_create(self):
        """
        Create a new character using the API request.
        Ensure that the record is created, and the returned token equals the one in the database
        """
        url = reverse('api:character_collection')
        self.client.force_authenticate(self._get_user())
        data = {
            'avatar_url': 'https://img.savageaim.com/test123',
            'lodestone_id': '3412557245',
            'name': 'Create Test',
            'world': 'Zodiark',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.content)
        self.assertEqual(Character.objects.count(), 1)
        char = Character.objects.first()
        data['id'] = char.pk
        data['verified'] = False
        data['user_id'] = self._get_user().id
        obj_data = CharacterCollectionSerializer(char).data
        self.assertDictEqual(data, obj_data)

        self.assertEqual(response.json()['id'], char.pk)

    def test_create_400(self):
        """
        Send requests to the create endpoint that are invalid.
        Ensure the appropriate error messages are returned for each case

        Some errors worth testing;
            - Create request for an existing lodestone id
            - omitting some data
        """
        url = reverse('api:character_collection')
        self.client.force_authenticate(self._get_user())

        # Omit all data and ensure request fails
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        errors = response.json()
        for field in ['avatar_url', 'lodestone_id', 'name', 'world']:
            self.assertTrue(field in errors, f'"{field}"" missing from errors; {errors}')
            self.assertEqual(errors[field], ['This field is required.'])

        # Try a valid request for a character that already exists
        char = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=self._get_user(),
            name='Char 1',
            world='Lich',
            verified=True,
        )

        data = CharacterCollectionSerializer(char).data
        data.pop('id')

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        errors = response.json()
        self.assertTrue('lodestone_id' in errors)
        self.assertEqual(errors['lodestone_id'], ['A verified character with this Lodestone ID already exists.'])


class CharacterResource(SavageAimTestCase):
    """
    Test the read method, and ensure correct data is returned
    """

    def tearDown(self):
        """
        Clean up the DB after each test
        """
        Character.objects.all().delete()

    def test_read(self):
        """
        Create a couple of characters for a user and send a list request for them
        ensure the data is returned as expected
        """
        user = self._get_user()
        self.client.force_authenticate(user)

        # Call management commands for the bislist
        call_command('job_seed', stdout=StringIO())
        call_command('gear_seed', stdout=StringIO())

        # Create some users, then send a list request and check the data returned is correct
        char = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=user,
            name='Char 1',
            world='Lich',
        )
        # Create a bislist for the character as well
        bis_gear = Gear.objects.first()
        curr_gear = Gear.objects.last()
        BISList.objects.create(
            bis_body=bis_gear,
            bis_bracelet=bis_gear,
            bis_earrings=bis_gear,
            bis_feet=bis_gear,
            bis_hands=bis_gear,
            bis_head=bis_gear,
            bis_left_ring=bis_gear,
            bis_legs=bis_gear,
            bis_mainhand=bis_gear,
            bis_necklace=bis_gear,
            bis_offhand=bis_gear,
            bis_right_ring=bis_gear,
            current_body=curr_gear,
            current_bracelet=curr_gear,
            current_earrings=curr_gear,
            current_feet=curr_gear,
            current_hands=curr_gear,
            current_head=curr_gear,
            current_left_ring=curr_gear,
            current_legs=curr_gear,
            current_mainhand=curr_gear,
            current_necklace=curr_gear,
            current_offhand=curr_gear,
            current_right_ring=curr_gear,
            job=Job.objects.get(pk='DRG'),
            owner=char,
        )
        url = reverse('api:character_resource', kwargs={'pk': char.id})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        content = response.json()
        self.assertDictEqual(content, CharacterDetailsSerializer(char).data)
        self.assertIn('bis_lists', content)
        self.assertEqual(len(content['bis_lists']), 1)

    # def test_delete(self):
    #     """
    #     Attempt to delete a character, then ensure it's missing from the DB
    #     """
    #     user = self._get_user()
    #     self.client.force_authenticate(user)

    #     # Create some users, then send a list request and check the data returned is correct
    #     char = Character.objects.create(
    #         avatar_url='https://img.savageaim.com/abcde',
    #         lodestone_id=1234567890,
    #         user=user,
    #         name='Char 1',
    #         world='Lich',
    #     )
    #     url = reverse('api:character_resource', kwargs={'pk': char.id})

    #     response = self.client.delete(url)
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, response.content)
    #     with self.assertRaises(Character.DoesNotExist):
    #         Character.objects.get(pk=char.pk)

    def test_404(self):
        """
        Test the cases that cause a 404 to be returned;

        - ID doesn't exist
        - Character doesn't belong to specified User
        """
        user = self._get_user()
        self.client.force_authenticate(user)

        # ID doesn't exist
        url = reverse('api:character_resource', kwargs={'pk': 0000000000000000000000})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.content)
        # response = self.client.delete(url)
        # self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.content)

        # Character belongs to a different user
        char = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=self._create_user(),
            name='Char 1',
            world='Lich',
        )
        url = reverse('api:character_resource', kwargs={'pk': char.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.content)
        # response = self.client.delete(url)
        # self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.content)


class CharacterVerification(SavageAimTestCase):
    """
    Test that the verification view works as intended
    """

    def tearDown(self):
        """
        Clean up the DB after each test
        """
        Character.objects.all().delete()

    @patch('api.views.character.verify_character.delay', side_effect=_fake_task)
    def test_verify(self, mocked_task):
        """
        Create a couple of characters for a user and send a list request for them
        ensure the data is returned as expected
        """
        user = self._get_user()
        self.client.force_authenticate(user)

        # Create some users, then send a list request and check the data returned is correct
        char = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=user,
            name='Char 1',
            world='Lich',
        )
        url = reverse('api:character_verification', kwargs={'pk': char.id})

        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED, response.content)
        char.refresh_from_db()
        self.assertTrue(char.verified)

        # Do some testing of the mocked task information
        mocked_task.assert_called()

    @patch('api.views.character.verify_character.delay', side_effect=_fake_task)
    def test_404(self, mocked_task):
        """
        Test the cases that cause a 404 to be returned;

        - ID doesn't exist
        - Character doesn't belong to specified User
        - Character is already verified
        """
        user = self._get_user()
        self.client.force_authenticate(user)

        # ID doesn't exist
        url = reverse('api:character_verification', kwargs={'pk': 0000000000000000000000})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.content)

        # Character belongs to a different user
        char = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=self._create_user(),
            name='Char 1',
            world='Lich',
        )
        url = reverse('api:character_verification', kwargs={'pk': char.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.content)

        # Character is already verified
        char.verified = True
        char.user = user
        char.save()
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.content)

        # Make sure the celery task was never called
        mocked_task.assert_not_called()
