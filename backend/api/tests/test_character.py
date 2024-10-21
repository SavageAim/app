# stdlib
from io import StringIO
from unittest.mock import patch
# lib
from django.core.management import call_command
from django.urls import reverse
from rest_framework import status
# local
from api import notifier
from api.models import BISList, Character, Gear, Notification, Job, Settings, Team, Tier
from api.serializers import CharacterCollectionSerializer, CharacterDetailsSerializer
from .test_base import SavageAimTestCase


def _fake_task(pk: int):
    """
    Handle what celery would handle if it were running
    """
    try:
        obj = Character.objects.get(pk=pk)
    except Character.DoesNotExist:  # pragma: no cover
        return
    if not obj.verified:
        obj.verified = True
        obj.save()
        notifier.verify_success(obj)
    else:
        notifier.verify_fail(obj, 'Already Verified!')


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
            'world': 'Zodiark (Light)',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.content)
        self.assertEqual(Character.objects.count(), 1)
        char = Character.objects.first()
        data['id'] = char.pk
        data['verified'] = False
        data['user_id'] = self._get_user().id
        data['alias'] = ''
        data['proxy'] = False
        data['bis_lists'] = []
        obj_data = CharacterCollectionSerializer(char).data
        self.assertDictEqual(data, obj_data)

        self.assertEqual(response.json()['id'], char.pk)
        char.delete()

        # Test with the new form of world text we're getting from lodestone and ensure my fix works
        data = {
            'avatar_url': 'https://img.savageaim.com/test123',
            'lodestone_id': '3412557245',
            'name': 'Create Test 2',
            'world': 'Lich [Light] ()',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.content)
        self.assertEqual(Character.objects.count(), 1)
        char = Character.objects.first()
        self.assertEqual(char.world, 'Lich (Light)')

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
    Test the resource methods, read and update, for correct action
    """

    def setUp(self):
        """
        Create user and BIS List
        """
        # Call management commands for the bislist
        call_command('seed', stdout=StringIO())

        # Create some users, then send a list request and check the data returned is correct
        self.char = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=self._get_user(),
            name='Char 1',
            world='Lich',
            verified=False,
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
            owner=self.char,
        )

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
        url = reverse('api:character_resource', kwargs={'pk': self.char.id})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        content = response.json()
        self.assertDictEqual(content, CharacterDetailsSerializer(self.char).data)
        self.assertIn('bis_lists', content)
        self.assertEqual(len(content['bis_lists']), 1)

    def test_update(self):
        """
        Test the update of a character's fields that can be updated
        """
        user = self._get_user()
        self.client.force_authenticate(user)
        url = reverse('api:character_resource', kwargs={'pk': self.char.id})

        data = {
            'alias': 'New Alias',
            'name': 'Test Character',
            'world': 'Lich 2 Electric Boogaloo',
            'avatar_url': 'https://savageaim.com',
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, response.content)
        self.char.refresh_from_db()
        self.assertEqual(self.char.alias, data['alias'])
        self.assertEqual(self.char.avatar_url, data['avatar_url'])
        self.assertEqual(self.char.name, data['name'])
        self.assertEqual(self.char.world, data['world'])

    def test_update_400(self):
        """
        Test that invalid update requests return 400 and the proper errors;
        - alias longer than 64 characters
        - avatar_url not a url
        - name longer than 60 characters
        - world longer than 60 characters
        """
        user = self._get_user()
        self.client.force_authenticate(user)
        url = reverse('api:character_resource', kwargs={'pk': self.char.id})

        data = {
            'alias': 'New Alias' * 64,
        }
        response = self.client.put(url, data)
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data['alias'], ['Ensure this field has no more than 64 characters.'])
        self.assertEqual(response_data['avatar_url'], ['This field is required.'])
        self.assertEqual(response_data['name'], ['This field is required.'])
        self.assertEqual(response_data['world'], ['This field is required.'])

        data = {'avatar_url': 'abcde' * 120}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['avatar_url'], ['Enter a valid URL.'])

        data = {'name': 'abcde' * 120}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['name'], ['Ensure this field has no more than 60 characters.'])

        data = {'world': 'abcde' * 120}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['world'], ['Ensure this field has no more than 60 characters.'])

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
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.content)

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
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.content)


class CharacterVerification(SavageAimTestCase):
    """
    Test that the verification view works as intended
    """

    def tearDown(self):
        """
        Clean up the DB after each test
        """
        Notification.objects.all().delete()
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

        # Check Notifications
        self.assertEqual(Notification.objects.filter(user=user).count(), 1)
        notif = Notification.objects.filter(user=user).first()
        self.assertEqual(notif.link, f'/characters/{char.id}/')
        self.assertEqual(notif.text, f'The verification of {char} has succeeded!')
        self.assertEqual(notif.type, 'verify_success')
        self.assertFalse(notif.read)

    def test_verify_fail_notifs(self):
        """
        Just call the mock task with a verified character and test the notifier task works
        Also test after changing the notif settings to ensure a second notif isn't sent
        """
        user = self._get_user_without_settings()
        char = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=user,
            name='Char 1',
            world='Lich',
            verified=True,
        )
        _fake_task(char.id)

        # Check Notification was created properly
        self.assertEqual(Notification.objects.filter(user=user).count(), 1)
        notif = Notification.objects.filter(user=user).first()
        self.assertEqual(notif.link, f'/characters/{char.id}/')
        self.assertEqual(notif.text, f'The verification of {char} has failed! Reason: Already Verified!')
        self.assertEqual(notif.type, 'verify_fail')
        self.assertFalse(notif.read)

        # Update settings and try again
        Settings.objects.create(user=user, theme='beta', notifications={'verify_fail': False})
        _fake_task(char.id)
        self.assertEqual(Notification.objects.filter(user=user).count(), 1)

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


class CharacterDelete(SavageAimTestCase):
    """
    Test the methods in the Delete view for correct logic
    """

    def setUp(self):
        """
        Create necessary models
        """
        Notification.objects.all().delete()
        # Call management commands for the bislist
        call_command('seed', stdout=StringIO())

        # Create some users, then send a list request and check the data returned is correct
        self.char = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=self._get_user(),
            name='Char 1',
            world='Lich',
            verified=False,
        )
        # Create a bislist for the character as well
        bis_gear = Gear.objects.first()
        curr_gear = Gear.objects.last()
        self.bis = BISList.objects.create(
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
            owner=self.char,
        )

        # Create some extra data for proper testing
        self.other_char = Character.objects.create(
            avatar_url='https://img.savageaim.com/vwxyz',
            lodestone_id=987654321,
            user=self._create_user(),
            name='Char 2',
            world='Lich',
            verified=True,
        )
        self.other_bis = BISList.objects.create(
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
            job=Job.objects.get(pk='PLD'),
            owner=self.other_char,
        )

        self.solo_team = Team.objects.create(
            invite_code=Team.generate_invite_code(),
            name='One Man Team',
            tier=Tier.objects.first(),
        )
        self.my_team = Team.objects.create(
            invite_code=Team.generate_invite_code(),
            name='My Team',
            tier=Tier.objects.first(),
        )
        self.your_team = Team.objects.create(
            invite_code=Team.generate_invite_code(),
            name='Your Team',
            tier=Tier.objects.first(),
        )

        self.solo_team.members.create(character=self.char, bis_list=self.bis, lead=True)
        self.my_team.members.create(character=self.char, bis_list=self.bis, lead=True)
        self.your_team.members.create(character=self.char, bis_list=self.bis, lead=False)
        self.my_team.members.create(character=self.other_char, bis_list=self.other_bis, lead=False)
        self.your_team.members.create(character=self.other_char, bis_list=self.other_bis, lead=True)

    def tearDown(self):
        """
        Clean up the DB after each test
        """
        Team.objects.all().delete()
        Character.objects.all().delete()

    def test_read(self):
        """
        Create a couple of characters for a user and send a list request for them
        ensure the data is returned as expected
        """
        user = self._get_user()
        self.client.force_authenticate(user)

        url = reverse('api:character_delete', kwargs={'pk': self.char.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        content = response.json()
        expected = {
            self.solo_team.name: {
                'members': 1,
                'lead': True,
                'name': self.solo_team.name,
            },
            self.my_team.name: {
                'members': 2,
                'lead': True,
                'name': self.my_team.name,
            },
            self.your_team.name: {
                'members': 2,
                'lead': False,
                'name': self.your_team.name,
            },
        }

        for entry in content:
            self.assertDictEqual(entry, expected[entry['name']])

    def test_delete(self):
        """
        Delete a character and check that all information as expected has been updated
        """
        user = self._get_user()
        self.client.force_authenticate(user)
        url = reverse('api:character_delete', kwargs={'pk': self.char.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(Character.DoesNotExist):
            Character.objects.get(pk=self.char.pk)

        with self.assertRaises(Team.DoesNotExist):
            Team.objects.get(pk=self.solo_team.pk)

        with self.assertRaises(BISList.DoesNotExist):
            BISList.objects.get(pk=self.bis.pk)

        Character.objects.get(pk=self.other_char.pk)
        BISList.objects.get(pk=self.other_bis.pk)

        # Check that My Team and Your Team both have 1 member and they are the leader
        my_team = Team.objects.get(pk=self.my_team.pk)
        your_team = Team.objects.get(pk=self.your_team.pk)
        self.assertEqual(my_team.members.count(), 1)
        self.assertEqual(my_team.members.first().character.pk, self.other_char.pk)
        self.assertTrue(my_team.members.first().lead)
        self.assertEqual(your_team.members.count(), 1)
        self.assertEqual(your_team.members.first().character.pk, self.other_char.pk)
        self.assertTrue(your_team.members.first().lead)

        # Check notifications - Other Char should have three
        # 1 - My Team Lead, 2 - My Team Leave, 3 - Your Team Leave
        notifs = Notification.objects.filter(user=self.other_char.user)
        self.assertEqual(notifs.count(), 3)
        expected = {
            f'{self.char} has left {self.my_team.name}!',
            f'{self.char} has left {self.your_team.name}!',
            f'{self.other_char} has been made the Team Leader of {self.my_team.name}!',
        }
        received = {notif.text for notif in notifs}
        self.assertSetEqual(expected, received)

    def test_404(self):
        """
        Test the cases that cause a 404 to be returned;

        - ID doesn't exist
        - Character doesn't belong to specified User
        """
        user = self._get_user()
        self.client.force_authenticate(user)

        # ID doesn't exist
        url = reverse('api:character_delete', kwargs={'pk': 0000000000000000000000})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.content)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.content)

        # Character belongs to a different user
        char = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=self._create_user(),
            name='Char 1',
            world='Lich',
        )
        url = reverse('api:character_delete', kwargs={'pk': char.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.content)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.content)
