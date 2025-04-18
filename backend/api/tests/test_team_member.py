from io import StringIO
from django.core.management import call_command
from django.urls import reverse
from rest_framework import status
from api.models import BISList, Character, Gear, Notification, Team, Tier
from api.serializers import TeamMemberSerializer
from .test_base import SavageAimTestCase


class TeamMemberResource(SavageAimTestCase):
    """
    Test views related to TeamMember specific code
    """

    def setUp(self):
        """
        Prepopulate the DB with known data we can calculate off of
        """
        self.maxDiff = None
        call_command('seed', stdout=StringIO())

        # Create a Team first
        self.team = Team.objects.create(
            invite_code=Team.generate_invite_code(),
            name='Les Jambons',
            tier=Tier.objects.get(max_item_level=605),
        )

        # Create two characters belonging to separate users
        self.char = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=self._get_user(),
            name='Team Lead',
            verified=True,
            world='Lich',
        )
        self.char2 = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=self._get_user(),
            name='Main Tank',
            verified=False,
            world='Lich',
        )

        # Next, create two BIS lists for each character
        raid_weapon = Gear.objects.get(item_level=605, name='Asphodelos')
        raid_gear = Gear.objects.get(item_level=600, has_weapon=False)
        tome_gear = Gear.objects.get(item_level=600, has_weapon=True)
        crafted = Gear.objects.get(name='Classical')
        self.tl_main_bis = BISList.objects.create(
            bis_body=raid_gear,
            bis_bracelet=raid_gear,
            bis_earrings=raid_gear,
            bis_feet=raid_gear,
            bis_hands=tome_gear,
            bis_head=tome_gear,
            bis_left_ring=tome_gear,
            bis_legs=tome_gear,
            bis_mainhand=raid_weapon,
            bis_necklace=tome_gear,
            bis_offhand=raid_weapon,
            bis_right_ring=raid_gear,
            current_body=crafted,
            current_bracelet=crafted,
            current_earrings=crafted,
            current_feet=crafted,
            current_hands=crafted,
            current_head=crafted,
            current_left_ring=crafted,
            current_legs=crafted,
            current_mainhand=crafted,
            current_necklace=crafted,
            current_offhand=crafted,
            current_right_ring=crafted,
            job_id='SGE',
            owner=self.char,
        )
        self.tl_alt_bis = BISList.objects.create(
            bis_body=tome_gear,
            bis_bracelet=tome_gear,
            bis_earrings=tome_gear,
            bis_feet=tome_gear,
            bis_hands=raid_gear,
            bis_head=raid_gear,
            bis_left_ring=raid_gear,
            bis_legs=raid_gear,
            bis_mainhand=raid_weapon,
            bis_necklace=raid_gear,
            bis_offhand=raid_weapon,
            bis_right_ring=tome_gear,
            current_body=crafted,
            current_bracelet=crafted,
            current_earrings=crafted,
            current_feet=crafted,
            current_hands=crafted,
            current_head=crafted,
            current_left_ring=crafted,
            current_legs=crafted,
            current_mainhand=crafted,
            current_necklace=crafted,
            current_offhand=crafted,
            current_right_ring=crafted,
            job_id='PLD',
            owner=self.char,
        )
        self.mt_main_bis = BISList.objects.create(
            bis_body=tome_gear,
            bis_bracelet=tome_gear,
            bis_earrings=tome_gear,
            bis_feet=tome_gear,
            bis_hands=raid_gear,
            bis_head=raid_gear,
            bis_left_ring=raid_gear,
            bis_legs=raid_gear,
            bis_mainhand=raid_weapon,
            bis_necklace=raid_gear,
            bis_offhand=raid_weapon,
            bis_right_ring=tome_gear,
            current_body=crafted,
            current_bracelet=crafted,
            current_earrings=crafted,
            current_feet=crafted,
            current_hands=crafted,
            current_head=crafted,
            current_left_ring=crafted,
            current_legs=crafted,
            current_mainhand=crafted,
            current_necklace=crafted,
            current_offhand=crafted,
            current_right_ring=crafted,
            job_id='PLD',
            owner=self.char2,
        )
        self.mt_alt_bis = BISList.objects.create(
            bis_body=raid_gear,
            bis_bracelet=raid_gear,
            bis_earrings=raid_gear,
            bis_feet=raid_gear,
            bis_hands=tome_gear,
            bis_head=tome_gear,
            bis_left_ring=tome_gear,
            bis_legs=tome_gear,
            bis_mainhand=raid_weapon,
            bis_necklace=tome_gear,
            bis_offhand=raid_weapon,
            bis_right_ring=raid_gear,
            current_body=crafted,
            current_bracelet=crafted,
            current_earrings=crafted,
            current_feet=crafted,
            current_hands=crafted,
            current_head=crafted,
            current_left_ring=crafted,
            current_legs=crafted,
            current_mainhand=crafted,
            current_necklace=crafted,
            current_offhand=crafted,
            current_right_ring=crafted,
            job_id='WHM',
            owner=self.char2,
        )

        # Lastly, link the characters to the team
        self.tm = self.team.members.create(character=self.char, bis_list=self.tl_main_bis, lead=True)

    def test_read(self):
        """
        Attempt to read the record and ensure the response is as expected
        """
        url = reverse('api:team_member_resource', kwargs={'team_id': self.team.pk, 'pk': self.tm.pk})
        user = self._get_user()
        self.client.force_authenticate(user)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected = TeamMemberSerializer(self.tm).data
        self.assertDictEqual(response.json(), expected)
        self.assertTrue(response.json()['permissions']['loot_manager'])
        self.assertTrue(response.json()['permissions']['proxy_manager'])

    def test_read_permissions(self):
        """
        Check each value of permissions to ensure the correct response is returned from the api
        """
        url = reverse('api:team_member_resource', kwargs={'team_id': self.team.pk, 'pk': self.tm.pk})
        user = self._get_user()
        self.client.force_authenticate(user)
        self.tm.lead = False
        self.tm.permissions = 2
        self.tm.save()

        expected = {
            'loot_manager': False,
            'proxy_manager': True,
        }
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.json()['permissions'], expected)

        self.tm.permissions = 1
        self.tm.save()
        expected = {
            'loot_manager': True,
            'proxy_manager': False,
        }
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.json()['permissions'], expected)

        self.tm.permissions = 0
        self.tm.save()
        expected = {
            'loot_manager': False,
            'proxy_manager': False,
        }
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.json()['permissions'], expected)

        self.tm.permissions = 3
        self.tm.save()
        expected = {
            'loot_manager': True,
            'proxy_manager': True,
        }
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.json()['permissions'], expected)

    def test_update(self):
        """
        Attempt a couple of updates to the Team Member object;

        First, try changing only the BIS List
        Then change the character and BIS List
        """
        url = reverse('api:team_member_resource', kwargs={'team_id': self.team.pk, 'pk': self.tm.pk})
        user = self._get_user()
        self.client.force_authenticate(user)

        data = {
            'character_id': self.char.pk,
            'bis_list_id': self.tl_alt_bis.pk,
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, response.content)
        self.tm.refresh_from_db()
        self.assertEqual(self.tm.character, self.char)
        self.assertEqual(self.tm.bis_list, self.tl_alt_bis)

        data = {
            'character_id': self.char2.pk,
            'bis_list_id': self.mt_main_bis.pk,
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, response.content)
        self.tm.refresh_from_db()
        self.assertEqual(self.tm.character, self.char2)
        self.assertEqual(self.tm.bis_list, self.mt_main_bis)

    def test_delete(self):
        """
        Attempt to test both Kick and Leave requests for a Team Member

        First have the team leader leave, and ensure the other character is now the Team Leader
        Then re-add the character that left, and have the Team Leader send a request to kick the user
        Note - Set char2's user to a new random user
        """
        self.char2.user = self._create_user()
        self.char2.save()
        tm2 = self.team.members.create(character=self.char2, bis_list=self.mt_main_bis, lead=False)

        # Part 1 - Have the leader leave the Team, ensure that char2 is now leader and is the only one in the Team
        url = reverse('api:team_member_resource', kwargs={'team_id': self.team.pk, 'pk': self.tm.pk})
        self.client.force_authenticate(self.char.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, response.content)

        self.team.refresh_from_db()
        self.assertEqual(self.team.members.count(), 1)
        tm2.refresh_from_db()
        self.assertTrue(tm2.lead)

        # Check notifications; char2's user should have 2 - one for new team lead, one for char leaving
        notifs = Notification.objects.filter(user=self.char2.user)
        self.assertEqual(notifs.count(), 2)
        self.assertSetEqual({n.type for n in notifs}, {'team_leave', 'team_lead'})

        # Return the other character to the Team and kick them from it
        self.tm = self.team.members.create(character=self.char, bis_list=self.tl_main_bis, lead=False)
        self.team.refresh_from_db()
        self.assertEqual(self.team.members.count(), 2)

        # Now send a delete request as the team leader's user
        url = reverse('api:team_member_resource', kwargs={'team_id': self.team.pk, 'pk': self.tm.pk})
        self.client.force_authenticate(self.char2.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, response.content)

        self.team.refresh_from_db()
        self.assertEqual(self.team.members.count(), 1)

        notifs = Notification.objects.filter(user=self.char2.user)
        self.assertEqual(notifs.count(), 2)
        notifs = Notification.objects.filter(user=self.char.user)
        self.assertEqual(notifs.count(), 1)
        self.assertEqual(notifs.first().text, f'{self.char} has been kicked from {self.team.name}!')

    def test_delete_proxy(self):
        """
        Make a Proxy character to ensure they can be kicked and will be deleted
        """
        self.char2.user = None
        self.char2.verified = False
        self.char2.save()
        tm2 = self.team.members.create(character=self.char2, bis_list=self.mt_main_bis, lead=False)
        self.assertIsNotNone(self.char.user)
        # Char 2 is a proxy, now if we kick them they should be deleted entirely
        url = reverse('api:team_member_resource', kwargs={'team_id': self.team.pk, 'pk': tm2.pk})
        self.client.force_authenticate(self.char.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, response.content)

        self.team.refresh_from_db()
        self.assertEqual(self.team.members.count(), 1)
        with self.assertRaises(Character.DoesNotExist):
            Character.objects.get(pk=self.char2.pk)

    def test_delete_proxy_with_permission(self):
        """
        Make a Proxy character to ensure they can be kicked and will be deleted
        Run this test as a non lead user with the proxy manager permission
        """
        self.char2.user = None
        self.char2.verified = False
        self.char2.save()
        tm2 = self.team.members.create(character=self.char2, bis_list=self.mt_main_bis, lead=False)
        self.assertIsNotNone(self.char.user)

        # Create a non lead user that has permission to use proxy manager
        char3 = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=self._create_user(),
            name='Main Tank',
            verified=True,
            world='Lich',
        )

        # Next, create two BIS lists for each character
        raid_weapon = Gear.objects.get(item_level=605, name='Asphodelos')
        raid_gear = Gear.objects.get(item_level=600, has_weapon=False)
        tome_gear = Gear.objects.get(item_level=600, has_weapon=True)
        crafted = Gear.objects.get(name='Classical')
        bis = BISList.objects.create(
            bis_body=raid_gear,
            bis_bracelet=raid_gear,
            bis_earrings=raid_gear,
            bis_feet=raid_gear,
            bis_hands=tome_gear,
            bis_head=tome_gear,
            bis_left_ring=tome_gear,
            bis_legs=tome_gear,
            bis_mainhand=raid_weapon,
            bis_necklace=tome_gear,
            bis_offhand=raid_weapon,
            bis_right_ring=raid_gear,
            current_body=crafted,
            current_bracelet=crafted,
            current_earrings=crafted,
            current_feet=crafted,
            current_hands=crafted,
            current_head=crafted,
            current_left_ring=crafted,
            current_legs=crafted,
            current_mainhand=crafted,
            current_necklace=crafted,
            current_offhand=crafted,
            current_right_ring=crafted,
            job_id='SGE',
            owner=char3,
        )
        self.team.members.create(character=char3, bis_list=bis, lead=False, permissions=3)

        # Ensure deletion still works
        url = reverse('api:team_member_resource', kwargs={'team_id': self.team.pk, 'pk': tm2.pk})
        self.client.force_authenticate(char3.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, response.content)

        self.team.refresh_from_db()
        self.assertEqual(self.team.members.count(), 2)
        with self.assertRaises(Character.DoesNotExist):
            Character.objects.get(pk=self.char2.pk)

    def test_leave_with_proxy(self):
        """
        Have one real and one proxy in a Team.
        Send a request for the real character to leave the team.
        Ensure that the proxy character is completely deleted along with the Team.
        """
        self.char2.user = None
        self.char2.save()
        self.team.members.create(character=self.char2, bis_list=self.mt_main_bis, lead=False)

        # Part 1 - Have the leader leave the Team, ensure that the Team and all Proxy data are gone
        url = reverse('api:team_member_resource', kwargs={'team_id': self.team.pk, 'pk': self.tm.pk})
        self.client.force_authenticate(self.char.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, response.content)

        with self.assertRaises(Team.DoesNotExist):
            Team.objects.get(pk=self.team.pk)
        with self.assertRaises(Character.DoesNotExist):
            Character.objects.get(pk=self.char2.pk)
        self.assertTrue(Character.objects.filter(pk=self.char.pk).exists())

    def test_404(self):
        """
        Test 404 responses for bad requests

        - Team ID doesn't exist
        - Team member pk not in team
        - Team member doesn't belong to user

        Delete specific:
        - User isn't team leader
        - Attempt to delete proxy without valid credentials
        """
        user = self._get_user()
        self.client.force_authenticate(user)

        url = reverse('api:team_member_resource', kwargs={'team_id': 'abcde', 'pk': self.tm.pk})
        self.assertEqual(self.client.get(url).status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(self.client.put(url).status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(self.client.delete(url).status_code, status.HTTP_404_NOT_FOUND)

        url = reverse('api:team_member_resource', kwargs={'team_id': self.team.pk, 'pk': '9999'})
        self.assertEqual(self.client.get(url).status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(self.client.put(url).status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(self.client.delete(url).status_code, status.HTTP_404_NOT_FOUND)

        self.char.user = self._create_user()
        self.char.save()
        url = reverse('api:team_member_resource', kwargs={'team_id': self.team.pk, 'pk': self.tm.pk})
        self.assertEqual(self.client.get(url).status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(self.client.put(url).status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(self.client.delete(url).status_code, status.HTTP_404_NOT_FOUND)

        self.char2.user = None
        self.char2.verified = False
        self.char2.save()
        tm2 = self.team.members.create(character=self.char2, bis_list=self.mt_main_bis, lead=False)
        url = reverse('api:team_member_resource', kwargs={'team_id': self.team.pk, 'pk': tm2.pk})
        self.assertEqual(self.client.delete(url).status_code, status.HTTP_404_NOT_FOUND)


class TeamMemberPermissionsResource(SavageAimTestCase):
    """
    Test views related to TeamMemberPermissions specific code
    """

    def setUp(self):
        """
        Prepopulate the DB with known data we can calculate off of
        """
        self.maxDiff = None
        call_command('seed', stdout=StringIO())

        # Create a Team first
        self.team = Team.objects.create(
            invite_code=Team.generate_invite_code(),
            name='Les Jambons',
            tier=Tier.objects.get(max_item_level=605),
        )

        # Create two characters belonging to separate users
        self.char = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=self._get_user(),
            name='Team Lead',
            verified=True,
            world='Lich',
        )
        self.char2 = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=self._get_user(),
            name='Main Tank',
            verified=False,
            world='Lich',
        )

        # Next, create two BIS lists for each character
        raid_weapon = Gear.objects.get(item_level=605, name='Asphodelos')
        raid_gear = Gear.objects.get(item_level=600, has_weapon=False)
        tome_gear = Gear.objects.get(item_level=600, has_weapon=True)
        crafted = Gear.objects.get(name='Classical')
        self.bis = BISList.objects.create(
            bis_body=raid_gear,
            bis_bracelet=raid_gear,
            bis_earrings=raid_gear,
            bis_feet=raid_gear,
            bis_hands=tome_gear,
            bis_head=tome_gear,
            bis_left_ring=tome_gear,
            bis_legs=tome_gear,
            bis_mainhand=raid_weapon,
            bis_necklace=tome_gear,
            bis_offhand=raid_weapon,
            bis_right_ring=raid_gear,
            current_body=crafted,
            current_bracelet=crafted,
            current_earrings=crafted,
            current_feet=crafted,
            current_hands=crafted,
            current_head=crafted,
            current_left_ring=crafted,
            current_legs=crafted,
            current_mainhand=crafted,
            current_necklace=crafted,
            current_offhand=crafted,
            current_right_ring=crafted,
            job_id='SGE',
            owner=self.char,
        )
        self.bis2 = BISList.objects.create(
            bis_body=tome_gear,
            bis_bracelet=tome_gear,
            bis_earrings=tome_gear,
            bis_feet=tome_gear,
            bis_hands=raid_gear,
            bis_head=raid_gear,
            bis_left_ring=raid_gear,
            bis_legs=raid_gear,
            bis_mainhand=raid_weapon,
            bis_necklace=raid_gear,
            bis_offhand=raid_weapon,
            bis_right_ring=tome_gear,
            current_body=crafted,
            current_bracelet=crafted,
            current_earrings=crafted,
            current_feet=crafted,
            current_hands=crafted,
            current_head=crafted,
            current_left_ring=crafted,
            current_legs=crafted,
            current_mainhand=crafted,
            current_necklace=crafted,
            current_offhand=crafted,
            current_right_ring=crafted,
            job_id='PLD',
            owner=self.char2,
        )

        # Lastly, link the characters to the team
        self.tm = self.team.members.create(character=self.char, bis_list=self.bis, lead=True)
        self.tm2 = self.team.members.create(character=self.char2, bis_list=self.bis2, lead=False)

    def test_update(self):
        """
        Set the permissions of a team member and ensure they are set correctly in the read response
        """
        url = reverse('api:team_member_permissions', kwargs={'team_id': self.team.pk, 'pk': self.tm2.pk})
        read_url = reverse('api:team_member_resource', kwargs={'team_id': self.team.pk, 'pk': self.tm2.pk})
        user = self._get_user()
        self.client.force_authenticate(user)

        data = {'permissions': 3}
        self.assertEqual(self.client.put(url, data).status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(read_url)
        self.assertTrue(response.json()['permissions']['loot_manager'])
        self.assertTrue(response.json()['permissions']['proxy_manager'])
        self.tm2.refresh_from_db()
        self.assertEqual(self.tm2.permissions, data['permissions'])

    def test_lead_update(self):
        """
        Attempt to set the permissions of a leader and ensure the DB doesn't change
        """
        url = reverse('api:team_member_permissions', kwargs={'team_id': self.team.pk, 'pk': self.tm.pk})
        read_url = reverse('api:team_member_resource', kwargs={'team_id': self.team.pk, 'pk': self.tm.pk})
        user = self._get_user()
        self.client.force_authenticate(user)

        data = {'permissions': 3}
        self.assertEqual(self.client.put(url, data).status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(read_url)
        self.assertTrue(response.json()['permissions']['loot_manager'])
        self.assertTrue(response.json()['permissions']['proxy_manager'])

        self.tm.refresh_from_db()
        self.assertEqual(self.tm.permissions, 0)

    def test_update_400(self):
        """
        Check that invalid permissions values are not allowed by the api
        Below 0 and greater than 3 currently are outside the range
        """
        url = reverse('api:team_member_permissions', kwargs={'team_id': self.team.pk, 'pk': self.tm2.pk})
        user = self._get_user()
        self.client.force_authenticate(user)

        data = {'permissions': -1}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()['permissions'],
            ['Invalid permissions value, this is more than likely a server error.'],
        )

        data = {'permissions': 4}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()['permissions'],
            ['Invalid permissions value, this is more than likely a server error.'],
        )

    def test_404(self):
        """
        Test 404 responses for bad requests

        - Team ID doesn't exist
        - Team member pk not in team
        - Requesting team member isn't leader
        """
        user = self._get_user()
        self.client.force_authenticate(user)

        url = reverse('api:team_member_permissions', kwargs={'team_id': 'abcde', 'pk': self.tm.pk})
        self.assertEqual(self.client.put(url).status_code, status.HTTP_404_NOT_FOUND)

        url = reverse('api:team_member_permissions', kwargs={'team_id': self.team.pk, 'pk': '9999'})
        self.assertEqual(self.client.put(url).status_code, status.HTTP_404_NOT_FOUND)

        self.char.user = self._create_user()
        self.char.save()
        url = reverse('api:team_member_permissions', kwargs={'team_id': self.team.pk, 'pk': self.tm.pk})
        self.assertEqual(self.client.put(url).status_code, status.HTTP_404_NOT_FOUND)


class TeamMemberCurrentGearResource(SavageAimTestCase):
    """
    Test views related to TeamMemberCurrentGear specific code
    """

    def setUp(self):
        """
        Prepopulate the DB with known data we can calculate off of
        """
        self.maxDiff = None
        call_command('seed', stdout=StringIO())

        # Create a Team first
        self.team = Team.objects.create(
            invite_code=Team.generate_invite_code(),
            name='Les Jambons',
            tier=Tier.objects.get(max_item_level=765),
        )

        # Create two characters belonging to separate users
        self.char = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=self._get_user(),
            name='Team Lead',
            verified=True,
            world='Lich',
        )
        self.char2 = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=22909725,
            user=self._get_user(),
            name='Not Team Lead',
            verified=False,
            world='Lich',
        )

        # Next, create two BIS lists for each character
        raid_weapon = Gear.objects.get(item_level=765, name='Babyface Champion')
        raid_gear = Gear.objects.get(item_level=760, has_weapon=False)
        tome_gear = Gear.objects.get(item_level=760, has_weapon=True)
        crafted = Gear.objects.get(name='Ceremonial')
        self.bis = BISList.objects.create(
            bis_body=raid_gear,
            bis_bracelet=raid_gear,
            bis_earrings=raid_gear,
            bis_feet=raid_gear,
            bis_hands=tome_gear,
            bis_head=tome_gear,
            bis_left_ring=tome_gear,
            bis_legs=tome_gear,
            bis_mainhand=raid_weapon,
            bis_necklace=tome_gear,
            bis_offhand=raid_weapon,
            bis_right_ring=raid_gear,
            current_body=crafted,
            current_bracelet=crafted,
            current_earrings=crafted,
            current_feet=crafted,
            current_hands=crafted,
            current_head=crafted,
            current_left_ring=crafted,
            current_legs=crafted,
            current_mainhand=crafted,
            current_necklace=crafted,
            current_offhand=crafted,
            current_right_ring=crafted,
            job_id='SGE',
            owner=self.char,
        )
        self.bis2 = BISList.objects.create(
            bis_body=tome_gear,
            bis_bracelet=tome_gear,
            bis_earrings=tome_gear,
            bis_feet=tome_gear,
            bis_hands=raid_gear,
            bis_head=raid_gear,
            bis_left_ring=raid_gear,
            bis_legs=raid_gear,
            bis_mainhand=raid_weapon,
            bis_necklace=raid_gear,
            bis_offhand=raid_weapon,
            bis_right_ring=tome_gear,
            current_body=crafted,
            current_bracelet=crafted,
            current_earrings=crafted,
            current_feet=crafted,
            current_hands=crafted,
            current_head=crafted,
            current_left_ring=crafted,
            current_legs=crafted,
            current_mainhand=crafted,
            current_necklace=crafted,
            current_offhand=crafted,
            current_right_ring=crafted,
            job_id='RDM',
            owner=self.char2,
        )

        # Lastly, link the characters to the team
        self.tm = self.team.members.create(character=self.char, bis_list=self.bis, lead=True)
        self.tm2 = self.team.members.create(character=self.char2, bis_list=self.bis2, lead=False)

    def test_update(self):
        """
        As the team leader, request an update of tm2's current gear from lodestone
        """
        url = reverse('api:team_member_current_gear_update', kwargs={'team_id': self.team.pk, 'pk': self.tm2.pk})
        user = self.char.user
        self.client.force_authenticate(user)
        self.assertEqual(self.client.post(url).status_code, status.HTTP_204_NO_CONTENT)

        # Check the Current Gear after a refresh
        self.bis2.refresh_from_db()
        self.assertEqual(self.bis2.current_mainhand.name, 'Voidvessel')
        self.assertEqual(self.bis2.current_head.name, 'Augmented Credendum')
        self.assertEqual(self.bis2.current_body.name, 'Augmented Credendum')
        self.assertEqual(self.bis2.current_hands.name, 'Augmented Credendum')
        self.assertEqual(self.bis2.current_legs.name, 'Augmented Credendum')
        self.assertEqual(self.bis2.current_feet.name, 'Augmented Credendum')
        self.assertEqual(self.bis2.current_earrings.name, 'Diadochos')
        self.assertEqual(self.bis2.current_necklace.name, 'Augmented Credendum')
        self.assertEqual(self.bis2.current_bracelet.name, 'Augmented Credendum')
        self.assertEqual(self.bis2.current_right_ring.name, 'Augmented Credendum')
        self.assertEqual(self.bis2.current_left_ring.name, 'Augmented Credendum')

    def test_errors(self):
        """
        Test any potential errors and error messages;
            - Could not find Lodestone character
            - Lodestone Job doesn't match the BIS Job
        """
        user = self.char.user
        self.client.force_authenticate(user)

        # Bad Character ID
        url = reverse('api:team_member_current_gear_update', kwargs={'team_id': self.team.pk, 'pk': self.tm.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Job ID doesn't match gear
        self.bis2.job_id = 'MNK'
        self.bis2.save()
        url = reverse('api:team_member_current_gear_update', kwargs={'team_id': self.team.pk, 'pk': self.tm2.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertTrue(
            'Couldn\'t import Gear from Lodestone. Gear was expected to be for "MNK"' in response.json()['message'],
        )

    def test_404(self):
        """
        Test 404 responses for bad requests

        - Team ID doesn't exist
        - Team member pk not in team
        - Requesting team member isn't leader
        """
        user = self._get_user()
        self.client.force_authenticate(user)

        url = reverse('api:team_member_current_gear_update', kwargs={'team_id': 'abcde', 'pk': self.tm.pk})
        self.assertEqual(self.client.post(url).status_code, status.HTTP_404_NOT_FOUND)

        url = reverse('api:team_member_current_gear_update', kwargs={'team_id': self.team.pk, 'pk': '9999'})
        self.assertEqual(self.client.post(url).status_code, status.HTTP_404_NOT_FOUND)

        self.char.user = self._create_user()
        self.char.save()
        url = reverse('api:team_member_current_gear_update', kwargs={'team_id': self.team.pk, 'pk': self.tm.pk})
        self.assertEqual(self.client.post(url).status_code, status.HTTP_404_NOT_FOUND)
