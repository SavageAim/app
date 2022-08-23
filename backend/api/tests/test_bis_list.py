# stdlib
from io import StringIO
# lib
from django.core.management import call_command
from django.urls import reverse
from rest_framework import status
# local
from api.models import BISList, Character, Gear, Team, Tier
from api.serializers import BISListSerializer
from .test_base import SavageAimTestCase


class BISListCollection(SavageAimTestCase):
    """
    Test the creation of new BISLists
    """

    def setUp(self):
        """
        Create a character for use in the test
        """
        self.char = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=self._get_user(),
            name='Char 1',
            world='Lich',
            verified=True,
        )
        call_command('seed', stdout=StringIO())

        self.gear_id_map = {g.name: g.id for g in Gear.objects.all()}

    def tearDown(self):
        """
        Clean up the DB after each test
        """
        Character.objects.all().delete()

    def test_create(self):
        """
        Create a new BIS List for the character
        """
        url = reverse('api:bis_collection', kwargs={'character_id': self.char.pk})
        self.client.force_authenticate(self.char.user)

        # Try one with PLD first
        data = {
            'job_id': 'PLD',
            'bis_mainhand_id': self.gear_id_map['Divine Light'],
            'bis_offhand_id': self.gear_id_map['Moonward'],
            'bis_head_id': self.gear_id_map['Limbo'],
            'bis_body_id': self.gear_id_map['Limbo'],
            'bis_hands_id': self.gear_id_map['Limbo'],
            'bis_legs_id': self.gear_id_map['Limbo'],
            'bis_feet_id': self.gear_id_map['Limbo'],
            'bis_earrings_id': self.gear_id_map['Limbo'],
            'bis_necklace_id': self.gear_id_map['Limbo'],
            'bis_bracelet_id': self.gear_id_map['Limbo'],
            'bis_right_ring_id': self.gear_id_map['Limbo'],
            'bis_left_ring_id': self.gear_id_map['Limbo'],
            'current_mainhand_id': self.gear_id_map['Moonward'],
            'current_offhand_id': self.gear_id_map['Moonward'],
            'current_head_id': self.gear_id_map['Moonward'],
            'current_body_id': self.gear_id_map['Moonward'],
            'current_hands_id': self.gear_id_map['Moonward'],
            'current_legs_id': self.gear_id_map['Moonward'],
            'current_feet_id': self.gear_id_map['Moonward'],
            'current_earrings_id': self.gear_id_map['Moonward'],
            'current_necklace_id': self.gear_id_map['Moonward'],
            'current_bracelet_id': self.gear_id_map['Moonward'],
            'current_right_ring_id': self.gear_id_map['Moonward'],
            'current_left_ring_id': self.gear_id_map['Moonward'],
            'external_link': '',
            'name': 'Hello :)',
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.content)
        self.assertEqual(BISList.objects.count(), 1)
        obj = BISList.objects.first()
        self.assertNotEqual(obj.bis_offhand_id, obj.bis_mainhand_id)
        self.assertIsNone(obj.external_link)
        obj.delete()

        # Do one for a different job, ensure that offhand and mainhand are actually the same
        data['job_id'] = 'SGE'
        data['external_link'] = 'https://etro.gg'
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.content)
        self.assertEqual(BISList.objects.count(), 1)
        obj = BISList.objects.first()
        self.assertEqual(obj.bis_offhand_id, obj.bis_mainhand_id)
        self.assertEqual(obj.bis_offhand_id, data['bis_mainhand_id'])
        self.assertEqual(obj.external_link, data['external_link'])

    def test_create_400(self):
        """
        Test all the kinds of errors that can come from the create endpoint;
            - Invalid number for a gear type
            - Gear pk doesn't exist
            - Gear category is incorrect
            - Job ID doesn't exist
            - Name too long
            - Data missing
            - External link isn't a url
        """
        url = reverse('api:bis_collection', kwargs={'character_id': self.char.pk})
        self.client.force_authenticate(self.char.user)

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.content)
        content = response.json()
        for field in content:
            self.assertEqual(content[field], ['This field is required.'])
        self.assertEqual(len(content), 26)

        # All gear errors will be run at once since there's only one actual function to test
        data = {
            'job_id': 'abc',
            'bis_mainhand_id': 'abcde',
            'bis_body_id': -1,
            'bis_head_id': self.gear_id_map['Eternal Dark'],
            'bis_earrings_id': self.gear_id_map['Divine Light'],
            'current_mainhand_id': self.gear_id_map['The Last'],
            'external_link': 'abcde',
            'name': 'abcde' * 100,
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.content)
        # Since we checked all the "this field is required" errors above, just check the ones we send now
        content = response.json()
        invalid_gear = 'The chosen type of Gear is invalid for this equipment slot.'
        self.assertEqual(content['job_id'], ['Please select a valid Job.'])
        self.assertEqual(content['bis_mainhand_id'], ['A valid integer is required.'])
        self.assertEqual(content['bis_body_id'], ['Please select a valid type of Gear.'])
        self.assertEqual(content['bis_head_id'], [invalid_gear])
        self.assertEqual(content['bis_earrings_id'], [invalid_gear])
        self.assertEqual(content['current_mainhand_id'], [invalid_gear])
        self.assertEqual(content['external_link'], ['Enter a valid URL.'])
        self.assertEqual(content['name'], ['Ensure this field has no more than 64 characters.'])

    def test_create_with_sync(self):
        """
        Test creating a list and also syncing the gear to another existing list at the same time
        """
        self.client.force_authenticate(self.char.user)

        # Create existing BIS Lists; one to sync and one that shouldn't because it's the wrong job
        sync_bis = BISList.objects.create(
            bis_body_id=self.gear_id_map['Augmented Radiant Host'],
            bis_bracelet_id=self.gear_id_map['Augmented Radiant Host'],
            bis_earrings_id=self.gear_id_map['Augmented Radiant Host'],
            bis_feet_id=self.gear_id_map['Augmented Radiant Host'],
            bis_hands_id=self.gear_id_map['Augmented Radiant Host'],
            bis_head_id=self.gear_id_map['Augmented Radiant Host'],
            bis_left_ring_id=self.gear_id_map['Augmented Radiant Host'],
            bis_legs_id=self.gear_id_map['Augmented Radiant Host'],
            bis_mainhand_id=self.gear_id_map['Augmented Radiant Host'],
            bis_necklace_id=self.gear_id_map['Augmented Radiant Host'],
            bis_offhand_id=self.gear_id_map['Augmented Radiant Host'],
            bis_right_ring_id=self.gear_id_map['Augmented Radiant Host'],
            current_body_id=self.gear_id_map['Moonward'],
            current_bracelet_id=self.gear_id_map['Moonward'],
            current_earrings_id=self.gear_id_map['Moonward'],
            current_feet_id=self.gear_id_map['Moonward'],
            current_hands_id=self.gear_id_map['Moonward'],
            current_head_id=self.gear_id_map['Moonward'],
            current_left_ring_id=self.gear_id_map['Moonward'],
            current_legs_id=self.gear_id_map['Moonward'],
            current_mainhand_id=self.gear_id_map['Moonward'],
            current_necklace_id=self.gear_id_map['Moonward'],
            current_offhand_id=self.gear_id_map['Moonward'],
            current_right_ring_id=self.gear_id_map['Moonward'],
            job_id='PLD',
            owner=self.char,
            external_link='https://etro.gg/',
        )
        non_sync_bis = BISList.objects.create(
            bis_body_id=self.gear_id_map['Augmented Radiant Host'],
            bis_bracelet_id=self.gear_id_map['Augmented Radiant Host'],
            bis_earrings_id=self.gear_id_map['Augmented Radiant Host'],
            bis_feet_id=self.gear_id_map['Augmented Radiant Host'],
            bis_hands_id=self.gear_id_map['Augmented Radiant Host'],
            bis_head_id=self.gear_id_map['Augmented Radiant Host'],
            bis_left_ring_id=self.gear_id_map['Augmented Radiant Host'],
            bis_legs_id=self.gear_id_map['Augmented Radiant Host'],
            bis_mainhand_id=self.gear_id_map['Augmented Radiant Host'],
            bis_necklace_id=self.gear_id_map['Augmented Radiant Host'],
            bis_offhand_id=self.gear_id_map['Augmented Radiant Host'],
            bis_right_ring_id=self.gear_id_map['Augmented Radiant Host'],
            current_body_id=self.gear_id_map['Moonward'],
            current_bracelet_id=self.gear_id_map['Moonward'],
            current_earrings_id=self.gear_id_map['Moonward'],
            current_feet_id=self.gear_id_map['Moonward'],
            current_hands_id=self.gear_id_map['Moonward'],
            current_head_id=self.gear_id_map['Moonward'],
            current_left_ring_id=self.gear_id_map['Moonward'],
            current_legs_id=self.gear_id_map['Moonward'],
            current_mainhand_id=self.gear_id_map['Moonward'],
            current_necklace_id=self.gear_id_map['Moonward'],
            current_offhand_id=self.gear_id_map['Moonward'],
            current_right_ring_id=self.gear_id_map['Moonward'],
            job_id='DRK',
            owner=self.char,
            external_link='https://etro.gg/',
        )

        data = {
            'job_id': 'PLD',
            'bis_mainhand_id': self.gear_id_map['Augmented Radiant Host'],
            'bis_offhand_id': self.gear_id_map['Augmented Radiant Host'],
            'bis_head_id': self.gear_id_map['Augmented Radiant Host'],
            'bis_body_id': self.gear_id_map['Augmented Radiant Host'],
            'bis_hands_id': self.gear_id_map['Augmented Radiant Host'],
            'bis_legs_id': self.gear_id_map['Augmented Radiant Host'],
            'bis_feet_id': self.gear_id_map['Augmented Radiant Host'],
            'bis_earrings_id': self.gear_id_map['Augmented Radiant Host'],
            'bis_necklace_id': self.gear_id_map['Augmented Radiant Host'],
            'bis_bracelet_id': self.gear_id_map['Augmented Radiant Host'],
            'bis_right_ring_id': self.gear_id_map['Augmented Radiant Host'],
            'bis_left_ring_id': self.gear_id_map['Augmented Radiant Host'],
            'current_mainhand_id': self.gear_id_map['Radiant Host'],
            'current_offhand_id': self.gear_id_map['Radiant Host'],
            'current_head_id': self.gear_id_map['Radiant Host'],
            'current_body_id': self.gear_id_map['Radiant Host'],
            'current_hands_id': self.gear_id_map['Radiant Host'],
            'current_legs_id': self.gear_id_map['Radiant Host'],
            'current_feet_id': self.gear_id_map['Radiant Host'],
            'current_earrings_id': self.gear_id_map['Radiant Host'],
            'current_necklace_id': self.gear_id_map['Radiant Host'],
            'current_bracelet_id': self.gear_id_map['Radiant Host'],
            'current_right_ring_id': self.gear_id_map['Radiant Host'],
            'current_left_ring_id': self.gear_id_map['Radiant Host'],
            'external_link': '',
            'name': 'Hello :)',
        }

        url = reverse('api:bis_collection', kwargs={'character_id': self.char.pk})
        response = self.client.post(f'{url}?sync={sync_bis.pk}&sync={non_sync_bis.pk}', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.content)
        sync_bis.refresh_from_db()
        non_sync_bis.refresh_from_db()
        self.assertEqual(sync_bis.current_body_id, self.gear_id_map['Radiant Host'])
        self.assertEqual(non_sync_bis.current_body_id, self.gear_id_map['Moonward'])

    def test_404(self):
        """
        Test all situations where the endpoint would respond with a 404;

        - Invalid ID
        - Character is not owned by the requesting user
        - Character is not verified
        """
        user = self._get_user()
        self.client.force_authenticate(user)

        # ID doesn't exist
        url = reverse('api:bis_collection', kwargs={'character_id': 0000000000000000000000})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.content)

        # Character belongs to a different user
        self.char.user = self._create_user()
        self.char.save()
        url = reverse('api:bis_collection', kwargs={'character_id': self.char.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.content)

        # Character is not verified
        self.char.verified = False
        self.char.user = user
        self.char.save()
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.content)


class BISListResource(SavageAimTestCase):
    """
    Test the update of existing BIS Lists
    """

    def setUp(self):
        """
        Create a character for use in the test
        """
        self.char = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=self._get_user(),
            name='Char 1',
            world='Lich',
            verified=True,
        )
        call_command('seed', stdout=StringIO())

        self.gear_id_map = {g.name: g.id for g in Gear.objects.all()}

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
            job_id='DRG',
            owner=self.char,
            external_link='https://etro.gg/',
        )

    def tearDown(self):
        """
        Clean up the DB after each test
        """
        Character.objects.all().delete()

    def test_read(self):
        """
        Read a BIS List via the API and ensure it is correctly returned
        """
        url = reverse('api:bis_resource', kwargs={'character_id': self.char.pk, 'pk': self.bis.pk})
        self.client.force_authenticate(self.char.user)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        self.assertDictEqual(response.json(), BISListSerializer(self.bis).data)

    def test_update(self):
        """
        Update the existing BIS List with a PUT request
        """
        url = reverse('api:bis_resource', kwargs={'character_id': self.char.pk, 'pk': self.bis.pk})
        self.client.force_authenticate(self.char.user)

        # Try one with PLD first
        data = {
            'job_id': 'PLD',
            'bis_mainhand_id': self.gear_id_map['Divine Light'],
            'bis_offhand_id': self.gear_id_map['Moonward'],
            'bis_head_id': self.gear_id_map['Limbo'],
            'bis_body_id': self.gear_id_map['Limbo'],
            'bis_hands_id': self.gear_id_map['Limbo'],
            'bis_legs_id': self.gear_id_map['Limbo'],
            'bis_feet_id': self.gear_id_map['Limbo'],
            'bis_earrings_id': self.gear_id_map['Limbo'],
            'bis_necklace_id': self.gear_id_map['Limbo'],
            'bis_bracelet_id': self.gear_id_map['Limbo'],
            'bis_right_ring_id': self.gear_id_map['Limbo'],
            'bis_left_ring_id': self.gear_id_map['Limbo'],
            'current_mainhand_id': self.gear_id_map['Moonward'],
            'current_offhand_id': self.gear_id_map['Moonward'],
            'current_head_id': self.gear_id_map['Moonward'],
            'current_body_id': self.gear_id_map['Moonward'],
            'current_hands_id': self.gear_id_map['Moonward'],
            'current_legs_id': self.gear_id_map['Moonward'],
            'current_feet_id': self.gear_id_map['Moonward'],
            'current_earrings_id': self.gear_id_map['Moonward'],
            'current_necklace_id': self.gear_id_map['Moonward'],
            'current_bracelet_id': self.gear_id_map['Moonward'],
            'current_right_ring_id': self.gear_id_map['Moonward'],
            'current_left_ring_id': self.gear_id_map['Moonward'],
            'external_link': None,
            'name': 'Update c:',
        }

        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, response.content)

        self.bis.refresh_from_db()
        self.assertEqual(self.bis.job_id, 'PLD')
        self.assertNotEqual(self.bis.bis_mainhand, self.bis.bis_offhand)
        self.assertIsNone(self.bis.external_link)
        self.assertEqual(self.bis.display_name, data['name'])

    def test_update_400(self):
        """
        Test all the kinds of errors that can come from the update endpoint;
            - Invalid number for a gear type
            - Gear pk doesn't exist
            - Gear category is incorrect
            - Job ID doesn't exist
            - Name is too long
            - Data missing
        """
        url = reverse('api:bis_resource', kwargs={'character_id': self.char.pk, 'pk': self.bis.pk})
        self.client.force_authenticate(self.char.user)

        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.content)
        content = response.json()
        for field in content:
            self.assertEqual(content[field], ['This field is required.'])
        self.assertEqual(len(content), 26)

        # All gear errors will be run at once since there's only one actual function to test
        data = {
            'job_id': 'abc',
            'bis_mainhand_id': 'abcde',
            'bis_body_id': -1,
            'bis_head_id': self.gear_id_map['Eternal Dark'],
            'bis_earrings_id': self.gear_id_map['Divine Light'],
            'current_mainhand_id': self.gear_id_map['The Last'],
            'name': 'abcde' * 64,
        }

        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.content)
        # Since we checked all the "this field is required" errors above, just check the ones we send now
        content = response.json()
        invalid_gear = 'The chosen type of Gear is invalid for this equipment slot.'
        self.assertEqual(content['job_id'], ['Please select a valid Job.'])
        self.assertEqual(content['bis_mainhand_id'], ['A valid integer is required.'])
        self.assertEqual(content['bis_body_id'], ['Please select a valid type of Gear.'])
        self.assertEqual(content['bis_head_id'], [invalid_gear])
        self.assertEqual(content['bis_earrings_id'], [invalid_gear])
        self.assertEqual(content['current_mainhand_id'], [invalid_gear])
        self.assertEqual(content['name'], ['Ensure this field has no more than 64 characters.'])

    def test_404(self):
        """
        Test all situations where the endpoint would respond with a 404;

        - Invalid Character ID
        - Character is not owned by the requesting user
        - Character is not verified
        - Invalid BISList ID
        - Character doesn't own BISList
        """
        user = self._get_user()
        self.client.force_authenticate(user)

        # ID doesn't exist
        url = reverse('api:bis_resource', kwargs={'character_id': 0000000000000000000000, 'pk': self.bis.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.content)
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.content)

        # Character belongs to a different user
        self.char.user = self._create_user()
        self.char.save()
        url = reverse('api:bis_resource', kwargs={'character_id': self.char.id, 'pk': self.bis.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.content)
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.content)

        # Character is not verified
        self.char.verified = False
        self.char.user = user
        self.char.save()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.content)
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.content)

        # Invalid BISList ID
        self.char.verified = True
        self.char.save()
        url = reverse('api:bis_resource', kwargs={'character_id': self.char.id, 'pk': 99999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.content)
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.content)

        # Character doesn't own BIS List
        char = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=self._get_user(),
            name='Char 2',
            world='Lich',
            verified=True,
        )
        self.bis.owner = char
        self.bis.save()
        url = reverse('api:bis_resource', kwargs={'character_id': self.char.id, 'pk': self.bis.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.content)
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.content)


class BISListDelete(SavageAimTestCase):
    """
    Tests for the delete methods
    """

    def setUp(self):
        """
        Create a character for use in the test
        """
        self.char = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=self._get_user(),
            name='Char 1',
            world='Lich',
            verified=True,
        )
        call_command('seed', stdout=StringIO())

        self.gear_id_map = {g.name: g.id for g in Gear.objects.all()}

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
            job_id='DRG',
            owner=self.char,
            external_link='https://etro.gg/',
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
            job_id='PLD',
            owner=self.char,
            external_link='https://etro.gg/',
        )

        self.team1 = Team.objects.create(
            invite_code=Team.generate_invite_code(),
            name='Team 1',
            tier=Tier.objects.first(),
        )
        self.team2 = Team.objects.create(
            invite_code=Team.generate_invite_code(),
            name='Team 2',
            tier=Tier.objects.first(),
        )

        self.team1.members.create(character=self.char, bis_list=self.bis, lead=True)
        self.team2.members.create(character=self.char, bis_list=self.other_bis, lead=True)

    def tearDown(self):
        """
        Clean up the DB after each test
        """
        Team.objects.all().delete()
        Character.objects.all().delete()

    def test_read(self):
        """
        - Create some Teams using the BIS List.
        - Send a read request to the delete endpoint
        - Ensure the expected response is returned
        """
        url = reverse('api:bis_delete', kwargs={'character_id': self.char.pk, 'pk': self.bis.pk})
        self.client.force_authenticate(self.char.user)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        content = response.json()

        expected = [{'name': self.team1.name, 'id': str(self.team1.id), 'member': self.team1.members.first().pk}]
        self.assertEqual(len(content), len(expected))
        self.assertDictEqual(content[0], expected[0])

    def test_delete(self):
        """
        - Attempt to delete a BIS List that isn't tied to any teams
        - Ensure the BIS no longer exists
        """
        url = reverse('api:bis_delete', kwargs={'character_id': self.char.pk, 'pk': self.other_bis.pk})
        self.client.force_authenticate(self.char.user)

        self.team2.delete()

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, response.content)
        with self.assertRaises(BISList.DoesNotExist):
            BISList.objects.get(pk=self.other_bis.pk)

    def test_delete_400(self):
        """
        - Attempt to delete a BIS List that is attached to a team
        - Ensure a 400 response is returned and the error message is correct
        """
        url = reverse('api:bis_delete', kwargs={'character_id': self.char.pk, 'pk': self.other_bis.pk})
        self.client.force_authenticate(self.char.user)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.content)
        self.assertEqual(response.json()['message'], 'Cannot delete; list is in use.')

        BISList.objects.get(pk=self.other_bis.pk)

    def test_404(self):
        """
        Test all situations where the endpoint would respond with a 404;

        - Invalid Character ID
        - Character is not owned by the requesting user
        - Character is not verified
        - Invalid BISList ID
        - Character doesn't own BISList
        """
        user = self._get_user()
        self.client.force_authenticate(user)

        # ID doesn't exist
        url = reverse('api:bis_delete', kwargs={'character_id': 0000000000000000000000, 'pk': self.bis.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.content)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.content)

        # Character belongs to a different user
        self.char.user = self._create_user()
        self.char.save()
        url = reverse('api:bis_delete', kwargs={'character_id': self.char.id, 'pk': self.bis.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.content)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.content)

        # Character is not verified
        self.char.verified = False
        self.char.user = user
        self.char.save()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.content)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.content)

        # Invalid BISList ID
        self.char.verified = True
        self.char.save()
        url = reverse('api:bis_delete', kwargs={'character_id': self.char.id, 'pk': 99999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.content)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.content)

        # Character doesn't own BIS List
        char = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=self._get_user(),
            name='Char 2',
            world='Lich',
            verified=True,
        )
        self.bis.owner = char
        self.bis.save()
        url = reverse('api:bis_delete', kwargs={'character_id': self.char.id, 'pk': self.bis.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.content)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.content)
