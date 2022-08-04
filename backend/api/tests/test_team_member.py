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
        call_command('tier_seed', stdout=StringIO())
        call_command('gear_seed', stdout=StringIO())
        call_command('job_seed', stdout=StringIO())

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
            verified=True,
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

    def test_leave_with_proxy(self):
        """
        Have one real and one proxy in a Team.
        Send a request for the real character to leave the team.
        Ensure that the proxy character is completely deleted along with the Team.
        """
        self.char2.user = None
        self.char2.save()
        tm2 = self.team.members.create(character=self.char2, bis_list=self.mt_main_bis, lead=False)

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
