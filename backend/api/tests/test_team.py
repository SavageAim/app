# stdlib
from io import StringIO
# lib
from django.core.management import call_command
from django.urls import reverse
from rest_framework import status
# local
from api.models import BISList, Character, Gear, Notification, Job, Team, TeamMember, Tier
from api.serializers import TeamSerializer
from .test_base import SavageAimTestCase


class TeamCollection(SavageAimTestCase):
    """
    Test the list and create methods
    """

    def setUp(self):
        """
        Run the seed commands, and create some necessary data
        """
        call_command('job_seed', stdout=StringIO())
        call_command('gear_seed', stdout=StringIO())
        call_command('tier_seed', stdout=StringIO())

        self.char = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=self._get_user(),
            name='Char 1',
            world='Lich',
        )
        g = Gear.objects.first()
        self.bis = BISList.objects.create(
            bis_body=g,
            bis_bracelet=g,
            bis_earrings=g,
            bis_feet=g,
            bis_hands=g,
            bis_head=g,
            bis_left_ring=g,
            bis_legs=g,
            bis_mainhand=g,
            bis_necklace=g,
            bis_offhand=g,
            bis_right_ring=g,
            current_body=g,
            current_bracelet=g,
            current_earrings=g,
            current_feet=g,
            current_hands=g,
            current_head=g,
            current_left_ring=g,
            current_legs=g,
            current_mainhand=g,
            current_necklace=g,
            current_offhand=g,
            current_right_ring=g,
            job=Job.objects.first(),
            owner=self.char,
        )

    def tearDown(self):
        """
        Clean up the DB after each test
        """
        TeamMember.objects.all().delete()
        Team.objects.all().delete()
        BISList.objects.all().delete()
        Character.objects.all().delete()

    def test_list(self):
        """
        Create a couple of characters for a user and send a list request for them
        ensure the data is returned as expected
        """
        url = reverse('api:team_collection')
        user = self._get_user()
        self.client.force_authenticate(user)

        # Create two teams, make the character a member of both
        team1 = Team.objects.create(
            invite_code=Team.generate_invite_code(),
            name='Test Team 1',
            tier=Tier.objects.first(),
        )
        team2 = Team.objects.create(
            invite_code=Team.generate_invite_code(),
            name='Test Team 2',
            tier=Tier.objects.first(),
        )
        # Test against data leakage
        Team.objects.create(
            invite_code=Team.generate_invite_code(),
            name='Test Team 3',
            tier=Tier.objects.first(),
        )
        TeamMember.objects.create(team=team1, character=self.char, bis_list=self.bis, lead=True)
        TeamMember.objects.create(team=team2, character=self.char, bis_list=self.bis, lead=False)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        content = response.json()
        self.assertEqual(len(content), 2)
        self.assertDictEqual(content[0], TeamSerializer(team1).data)
        self.assertDictEqual(content[1], TeamSerializer(team2).data)

    def test_list_filters(self):
        """
        Test the same as above but also ensure that the filtering works
        """
        base_url = reverse('api:team_collection')
        user = self._get_user()
        self.client.force_authenticate(user)

        # Create two teams, make the character a member of both
        team1 = Team.objects.create(
            invite_code=Team.generate_invite_code(),
            name='Test Team 1',
            tier=Tier.objects.first(),
        )
        team2 = Team.objects.create(
            invite_code=Team.generate_invite_code(),
            name='Test Team 2',
            tier=Tier.objects.first(),
        )
        TeamMember.objects.create(team=team1, character=self.char, bis_list=self.bis, lead=True)
        TeamMember.objects.create(team=team2, character=self.char, bis_list=self.bis, lead=False)

        # Test with character's id
        response = self.client.get(f'{base_url}?char_id={self.char.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        content = response.json()
        self.assertEqual(len(content), 2)

        # Test with different ID
        response = self.client.get(f'{base_url}?char_id=999')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        content = response.json()
        self.assertEqual(len(content), 0)

        # Test with letters and ensure full response is returned
        response = self.client.get(f'{base_url}?char_id=abcde')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        content = response.json()
        self.assertEqual(len(content), 2)

    def test_create(self):
        """
        Create a new Team in the database
        Ensure that the record is created, and the returned token equals the one in the database
        """
        url = reverse('api:team_collection')
        self.client.force_authenticate(self._get_user())

        self.char.verified = True
        self.char.save()
        data = {
            'name': 'Test',
            'tier_id': Tier.objects.first().pk,
            'bis_list_id': self.bis.id,
            'character_id': self.char.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.content)
        self.assertEqual(Team.objects.count(), 1)
        obj = Team.objects.first()
        self.assertEqual(response.json()['id'], str(obj.pk))

    def test_create_400(self):
        """
        Attempt to test creation of a Team with invalid data and ensure appropriate responses are returned

        Character ID Not Sent: 'This field is required.'
        Character ID Not Int:  'A valid integer is required.'
        Character ID Invalid: 'Please select a valid, verified Character that you own.'
        BIS List ID Not Sent: 'This field is required.'
        BIS List ID Not Int: 'A valid integer is required.'
        BIS List doesn't belong to any of your characters: 'Please select a valid BISList belonging to your Character.'
        BIS List doesn't belong to sent character: 'Please select a valid BISList belonging to your Character.'
        Name not sent: 'This field is required.'
        Name Too Long: 'Ensure this field has no more than 64 characters.'
        Tier ID Not Sent: 'This field is required.'
        Tier ID Not Int:  'A valid integer is required.'
        Tier ID Invalid: 'Please select a valid Tier.'
        """
        url = reverse('api:team_collection')
        self.client.force_authenticate(self._get_user())

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.content)
        content = response.json()
        self.assertEqual(content['name'], ['This field is required.'])
        self.assertEqual(content['tier_id'], ['This field is required.'])
        self.assertEqual(content['bis_list_id'], ['This field is required.'])
        self.assertEqual(content['character_id'], ['This field is required.'])

        data = {
            'character_id': 'abcde',
            'bis_list_id': 'abcde',
            'name': 'abcde' * 100,
            'tier_id': 'abcde',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.content)
        content = response.json()
        self.assertEqual(content['name'], ['Ensure this field has no more than 64 characters.'])
        self.assertEqual(content['tier_id'], ['A valid integer is required.'])
        self.assertEqual(content['bis_list_id'], ['A valid integer is required.'])
        self.assertEqual(content['character_id'], ['A valid integer is required.'])

        data = {
            'character_id': '90',
            'bis_list_id': '90',
            'name': 'abcde',
            'tier_id': '90',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.content)
        content = response.json()
        self.assertEqual(content['bis_list_id'], ['Please select a valid BISList belonging to your Character.'])
        self.assertEqual(content['character_id'], ['Please select a valid, verified Character that you own.'])
        self.assertEqual(content['tier_id'], ['Please select a valid Tier.'])

        # Test with valid unverified char, and someone elses' bis list
        char = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1348724213,
            user=self._create_user(),
            name='Char 2',
            world='Lich',
        )
        bis = BISList.objects.create(
            bis_body=Gear.objects.first(),
            bis_bracelet=Gear.objects.first(),
            bis_earrings=Gear.objects.first(),
            bis_feet=Gear.objects.first(),
            bis_hands=Gear.objects.first(),
            bis_head=Gear.objects.first(),
            bis_left_ring=Gear.objects.first(),
            bis_legs=Gear.objects.first(),
            bis_mainhand=Gear.objects.first(),
            bis_necklace=Gear.objects.first(),
            bis_offhand=Gear.objects.first(),
            bis_right_ring=Gear.objects.first(),
            current_body=Gear.objects.last(),
            current_bracelet=Gear.objects.last(),
            current_earrings=Gear.objects.last(),
            current_feet=Gear.objects.last(),
            current_hands=Gear.objects.last(),
            current_head=Gear.objects.last(),
            current_left_ring=Gear.objects.last(),
            current_legs=Gear.objects.last(),
            current_mainhand=Gear.objects.last(),
            current_necklace=Gear.objects.last(),
            current_offhand=Gear.objects.last(),
            current_right_ring=Gear.objects.last(),
            job=Job.objects.get(pk='DRG'),
            owner=char,
        )
        data = {
            'character_id': self.char.id,
            'bis_list_id': bis.id,
            'name': 'Test',
            'tier_id': Tier.objects.first().pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.content)
        content = response.json()
        self.assertEqual(content['character_id'], ['Please select a valid, verified Character that you own.'])
        self.assertEqual(content['bis_list_id'], ['Please select a valid BISList belonging to your Character.'])

        # Lastly check the top level validate error
        char.user = self._get_user()
        char.save()
        self.char.verified = True
        self.char.save()
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.content)
        content = response.json()
        self.assertEqual(content['bis_list_id'], ['Please select a valid BISList belonging to your Character.'])


class TeamResource(SavageAimTestCase):
    """
    Test the read and update methods
    """

    def setUp(self):
        """
        Run the seed commands, and create some necessary data
        """
        call_command('job_seed', stdout=StringIO())
        call_command('gear_seed', stdout=StringIO())
        call_command('tier_seed', stdout=StringIO())

        self.char = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=self._get_user(),
            name='Char 1',
            world='Lich',
        )
        g = Gear.objects.first()
        self.bis = BISList.objects.create(
            bis_body=g,
            bis_bracelet=g,
            bis_earrings=g,
            bis_feet=g,
            bis_hands=g,
            bis_head=g,
            bis_left_ring=g,
            bis_legs=g,
            bis_mainhand=g,
            bis_necklace=g,
            bis_offhand=g,
            bis_right_ring=g,
            current_body=g,
            current_bracelet=g,
            current_earrings=g,
            current_feet=g,
            current_hands=g,
            current_head=g,
            current_left_ring=g,
            current_legs=g,
            current_mainhand=g,
            current_necklace=g,
            current_offhand=g,
            current_right_ring=g,
            job=Job.objects.first(),
            owner=self.char,
        )
        self.team = Team.objects.create(
            invite_code=Team.generate_invite_code(),
            name='Test Team 1',
            tier=Tier.objects.first(),
        )
        self.tm = TeamMember.objects.create(team=self.team, character=self.char, bis_list=self.bis, lead=True)

    def tearDown(self):
        """
        Clean up the DB after each test
        """
        Notification.objects.all().delete()
        TeamMember.objects.all().delete()
        Team.objects.all().delete()
        BISList.objects.all().delete()
        Character.objects.all().delete()

    def test_read(self):
        """
        Read the Team object as a user whose character is in the team
        """
        user = self._get_user()
        self.client.force_authenticate(user)
        url = reverse('api:team_resource', kwargs={'pk': self.team.id})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        content = response.json()
        self.assertDictEqual(content, TeamSerializer(self.team).data)
        self.assertIn('members', content)
        self.assertEqual(len(content['members']), 1)

    def test_regenerate_token(self):
        """
        Send a PATCH request to the endpoint, and ensure the team's invite code has changed
        """
        user = self._get_user()
        self.client.force_authenticate(user)
        url = reverse('api:team_resource', kwargs={'pk': self.team.id})

        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, response.content)
        with self.assertRaises(Team.DoesNotExist):
            Team.objects.get(invite_code=self.team.invite_code)

    def test_update(self):
        """
        Update the Team fully and ensure the data in the DB has been updated
        """
        user = self._get_user()
        self.client.force_authenticate(user)
        url = reverse('api:team_resource', kwargs={'pk': self.team.id})

        # Create required objects
        new_tier = Tier.objects.create(name='Memes', max_item_level=900, raid_gear_name='The End')
        char = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1348724213,
            user=self._create_user(),
            name='Char 2',
            world='Lich',
        )
        bis = BISList.objects.create(
            bis_body=Gear.objects.first(),
            bis_bracelet=Gear.objects.first(),
            bis_earrings=Gear.objects.first(),
            bis_feet=Gear.objects.first(),
            bis_hands=Gear.objects.first(),
            bis_head=Gear.objects.first(),
            bis_left_ring=Gear.objects.first(),
            bis_legs=Gear.objects.first(),
            bis_mainhand=Gear.objects.first(),
            bis_necklace=Gear.objects.first(),
            bis_offhand=Gear.objects.first(),
            bis_right_ring=Gear.objects.first(),
            current_body=Gear.objects.last(),
            current_bracelet=Gear.objects.last(),
            current_earrings=Gear.objects.last(),
            current_feet=Gear.objects.last(),
            current_hands=Gear.objects.last(),
            current_head=Gear.objects.last(),
            current_left_ring=Gear.objects.last(),
            current_legs=Gear.objects.last(),
            current_mainhand=Gear.objects.last(),
            current_necklace=Gear.objects.last(),
            current_offhand=Gear.objects.last(),
            current_right_ring=Gear.objects.last(),
            job=Job.objects.get(pk='DRG'),
            owner=char,
        )
        tm = TeamMember.objects.create(team=self.team, character=char, bis_list=bis, lead=False)

        # Send the request
        data = {
            'name': 'Updated Team Name',
            'tier_id': new_tier.id,
            'team_lead': char.id,
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, response.content)
        old_name = self.team.name

        # Ensure the Team has been updated
        self.team.refresh_from_db()
        self.assertEqual(self.team.name, data['name'])
        self.assertEqual(self.team.tier.id, new_tier.id)
        tm.refresh_from_db()
        self.assertTrue(tm.lead)
        self.tm.refresh_from_db()
        self.assertFalse(self.tm.lead)

        # Ensure the new character got a notification
        self.assertEqual(Notification.objects.filter(user=char.user).count(), 2)
        notifs = Notification.objects.filter(user=char.user)
        note_map = {
            'team_lead': f'{char} has been made the Team Leader of {self.team.name}!',
            'team_rename': f'{old_name} has been renamed to {self.team.name}!',
        }
        for notif in notifs:
            self.assertEqual(notif.link, f'/team/{self.team.id}/')
            self.assertEqual(notif.text, note_map[notif.type])
            self.assertFalse(notif.read)

    def test_update_400(self):
        """
        Send invalid update requests and ensure the right errors are returned from each request

        Name Not Sent: 'This field is required.'
        Name Too Long: 'Ensure this field has no more than 64 characters.'
        Tier ID Not Sent: 'This field is required.'
        Tier ID Not Int:  'A valid integer is required.'
        Tier ID Invalid: 'Please select a valid Tier.'
        Team Lead Not Sent: 'This field is required.'
        Team Lead Not Int: 'A valid integer is required.'
        Team Lead Invalid: 'Please select a non-proxy Member of the Team to be the new team lead.'
        Proxy Team Lead: 'Please select a non-proxy Member of the Team to be the new team lead.'
        """
        user = self._get_user()
        self.client.force_authenticate(user)
        url = reverse('api:team_resource', kwargs={'pk': self.team.id})

        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.content)
        content = response.json()
        self.assertEqual(content['name'], ['This field is required.'])
        self.assertEqual(content['tier_id'], ['This field is required.'])
        self.assertEqual(content['team_lead'], ['This field is required.'])

        data = {
            'name': 'abcde' * 100,
            'tier_id': 'abcde',
            'team_lead': 'abcde',
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.content)
        content = response.json()
        self.assertEqual(content['name'], ['Ensure this field has no more than 64 characters.'])
        self.assertEqual(content['tier_id'], ['A valid integer is required.'])
        self.assertEqual(content['team_lead'], ['A valid integer is required.'])

        data = {
            'name': 'Hi c:',
            'tier_id': 123,
            'team_lead': 123,
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.content)
        content = response.json()
        self.assertEqual(content['tier_id'], ['Please select a valid Tier.'])
        self.assertEqual(
            content['team_lead'],
            ['Please select a non-proxy Member of the Team to be the new team lead.'],
        )

        # Run the team lead test again with a valid character id that isn't on the team
        char = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1348724213,
            user=self._create_user(),
            name='Char 2',
            world='Lich',
        )
        data = {
            'name': 'Hi c:',
            'tier_id': Tier.objects.first().pk,
            'team_lead': char.id,
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.content)
        content = response.json()
        self.assertEqual(
            content['team_lead'],
            ['Please select a non-proxy Member of the Team to be the new team lead.'],
        )

        # Make the above Character a Member of the Team, but make them a proxy
        char.user = None
        char.save()
        g = Gear.objects.first()
        bis = BISList.objects.create(
            bis_body=g,
            bis_bracelet=g,
            bis_earrings=g,
            bis_feet=g,
            bis_hands=g,
            bis_head=g,
            bis_left_ring=g,
            bis_legs=g,
            bis_mainhand=g,
            bis_necklace=g,
            bis_offhand=g,
            bis_right_ring=g,
            current_body=g,
            current_bracelet=g,
            current_earrings=g,
            current_feet=g,
            current_hands=g,
            current_head=g,
            current_left_ring=g,
            current_legs=g,
            current_mainhand=g,
            current_necklace=g,
            current_offhand=g,
            current_right_ring=g,
            job=Job.objects.first(),
            owner=char,
        )
        self.team.members.create(character=char, bis_list=bis, lead=False)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.content)
        content = response.json()
        self.assertEqual(
            content['team_lead'],
            ['Please select a non-proxy Member of the Team to be the new team lead.'],
        )

    def test_delete(self):
        """
        Send a request to disband a Team.
        Ensure that other Members of the Team receive a disband notification as well
        """
        user = self._get_user()
        self.client.force_authenticate(user)
        url = reverse('api:team_resource', kwargs={'pk': self.team.id})

        other_char = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=987654321,
            user=self._create_user(),
            name='Char 2',
            world='Lich',
        )
        g = Gear.objects.first()
        other_bis = BISList.objects.create(
            bis_body=g,
            bis_bracelet=g,
            bis_earrings=g,
            bis_feet=g,
            bis_hands=g,
            bis_head=g,
            bis_left_ring=g,
            bis_legs=g,
            bis_mainhand=g,
            bis_necklace=g,
            bis_offhand=g,
            bis_right_ring=g,
            current_body=g,
            current_bracelet=g,
            current_earrings=g,
            current_feet=g,
            current_hands=g,
            current_head=g,
            current_left_ring=g,
            current_legs=g,
            current_mainhand=g,
            current_necklace=g,
            current_offhand=g,
            current_right_ring=g,
            job=Job.objects.last(),
            owner=other_char,
        )
        self.team.members.create(character=other_char, bis_list=other_bis, lead=False)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, response.content)

        with self.assertRaises(Team.DoesNotExist):
            Team.objects.get(pk=self.team.pk)

        self.assertEqual(Notification.objects.filter(user=user).count(), 0)
        user = other_char.user
        self.assertEqual(Notification.objects.filter(user=user).count(), 1)
        notif = Notification.objects.filter(user=user).first()
        self.assertEqual(notif.text, f'"{self.team.name}" has been disbanded!')

    def test_404(self):
        """
        Test the cases that cause a 404 to be returned;

        - ID doesn't exist
        - Read request from someone who doesn't have a character in the Team
        - Update request from someone who doesn't have a character in the Team
        - Update request from someone that isn't the team lead
        """
        user = self._get_user()
        self.client.force_authenticate(user)

        # ID doesn't exist
        url = reverse('api:team_resource', kwargs={'pk': 'abcde-abcde-abcde-abcde'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.content)
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.content)
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.content)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.content)

        url = reverse('api:team_resource', kwargs={'pk': self.team.id})
        # Check update as non-team lead
        self.tm.lead = False
        self.tm.save()
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.content)
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.content)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.content)

        # Delete membership altogether and test both read and update
        self.tm.delete()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.content)
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.content)
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.content)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.content)


class TeamInvite(SavageAimTestCase):
    """
    Test the Team Invite views work as we want them to
    """

    def setUp(self):
        """
        Run the seed commands, and create some necessary data
        """
        call_command('job_seed', stdout=StringIO())
        call_command('gear_seed', stdout=StringIO())
        call_command('tier_seed', stdout=StringIO())

        self.char = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=self._get_user(),
            name='Char 1',
            world='Lich',
        )
        g = Gear.objects.first()
        self.bis = BISList.objects.create(
            bis_body=g,
            bis_bracelet=g,
            bis_earrings=g,
            bis_feet=g,
            bis_hands=g,
            bis_head=g,
            bis_left_ring=g,
            bis_legs=g,
            bis_mainhand=g,
            bis_necklace=g,
            bis_offhand=g,
            bis_right_ring=g,
            current_body=g,
            current_bracelet=g,
            current_earrings=g,
            current_feet=g,
            current_hands=g,
            current_head=g,
            current_left_ring=g,
            current_legs=g,
            current_mainhand=g,
            current_necklace=g,
            current_offhand=g,
            current_right_ring=g,
            job=Job.objects.first(),
            owner=self.char,
        )
        self.team = Team.objects.create(
            invite_code=Team.generate_invite_code(),
            name='Test Team 1',
            tier=Tier.objects.first(),
        )

    def tearDown(self):
        """
        Clean up the DB after each test
        """
        Notification.objects.all().delete()
        TeamMember.objects.all().delete()
        Team.objects.all().delete()
        BISList.objects.all().delete()
        Character.objects.all().delete()

    def test_head(self):
        """
        Ensure the head method returns status 200 for a valid invite code, without having to be a Member
        """
        user = self._get_user()
        self.client.force_authenticate(user)
        url = reverse('api:team_invite', kwargs={'invite_code': self.team.invite_code})

        response = self.client.head(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)

    def test_read(self):
        """
        Ensure that anyone can read a team via its invite code
        """
        user = self._get_user()
        self.client.force_authenticate(user)
        url = reverse('api:team_invite', kwargs={'invite_code': self.team.invite_code})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        self.assertDictEqual(response.json(), TeamSerializer(self.team).data)

    def test_join(self):
        """
        Attempt to join a Team using a character and bis list
        """
        user = self._create_user()
        self.client.force_authenticate(user)
        url = reverse('api:team_invite', kwargs={'invite_code': self.team.invite_code})

        # Link the self.char to the team for notification checking
        TeamMember.objects.create(team=self.team, character=self.char, bis_list=self.bis, lead=True)

        # Create new details
        char = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=user,
            name='Char 1',
            world='Lich',
            verified=True,
        )
        g = Gear.objects.first()
        bis = BISList.objects.create(
            bis_body=g,
            bis_bracelet=g,
            bis_earrings=g,
            bis_feet=g,
            bis_hands=g,
            bis_head=g,
            bis_left_ring=g,
            bis_legs=g,
            bis_mainhand=g,
            bis_necklace=g,
            bis_offhand=g,
            bis_right_ring=g,
            current_body=g,
            current_bracelet=g,
            current_earrings=g,
            current_feet=g,
            current_hands=g,
            current_head=g,
            current_left_ring=g,
            current_legs=g,
            current_mainhand=g,
            current_necklace=g,
            current_offhand=g,
            current_right_ring=g,
            job=Job.objects.first(),
            owner=char,
        )

        data = {
            'character_id': char.id,
            'bis_list_id': bis.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.content)
        self.assertEqual(response.json()['id'], str(self.team.id))

        # Check that the self.user has a notification
        self.assertEqual(Notification.objects.filter(user=self.char.user).count(), 1)
        notif = Notification.objects.filter(user=self.char.user).first()
        self.assertEqual(notif.link, f'/team/{self.team.id}/')
        self.assertEqual(notif.text, f'{char} has joined {self.team.name}!')
        self.assertEqual(notif.type, 'team_join')
        self.assertFalse(notif.read)

    def test_join_400(self):
        """
        Attempt to join a Team using bad values and ensure 400 responses and correct errors are returned

        Character ID Sent: 'This field is required.'
        Character ID Not Int:  'A valid integer is required.'
        Character ID Invalid: 'Please select a valid, verified Character that you own.'
        Character already in team: 'This Character is already a member of the Team.'
        BIS List ID Not Sent: 'This field is required.'
        BIS List ID Not Int: 'A valid integer is required.'
        BIS List doesn't belong to any of your characters: 'Please select a valid BISList belonging to your Character.'
        BIS List doesn't belong to sent character: 'Please select a valid BISList belonging to your Character.'
        """
        user = self._get_user()
        self.client.force_authenticate(user)
        url = reverse('api:team_invite', kwargs={'invite_code': self.team.invite_code})

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.content)
        content = response.json()
        self.assertEqual(content['character_id'], ['This field is required.'])
        self.assertEqual(content['bis_list_id'], ['This field is required.'])

        data = {
            'character_id': 'abcde',
            'bis_list_id': 'abcde',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.content)
        content = response.json()
        self.assertEqual(content['character_id'], ['A valid integer is required.'])
        self.assertEqual(content['bis_list_id'], ['A valid integer is required.'])

        data = {
            'character_id': '999999999999',
            'bis_list_id': '999999999999',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.content)
        content = response.json()
        self.assertEqual(content['character_id'], ['Please select a valid, verified Character that you own.'])
        self.assertEqual(content['bis_list_id'], ['Please select a valid BISList belonging to your Character.'])

        # Test with valid unverified char, and someone elses' bis list
        char = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1348724213,
            user=self._create_user(),
            name='Char 2',
            world='Lich',
        )
        bis = BISList.objects.create(
            bis_body=Gear.objects.first(),
            bis_bracelet=Gear.objects.first(),
            bis_earrings=Gear.objects.first(),
            bis_feet=Gear.objects.first(),
            bis_hands=Gear.objects.first(),
            bis_head=Gear.objects.first(),
            bis_left_ring=Gear.objects.first(),
            bis_legs=Gear.objects.first(),
            bis_mainhand=Gear.objects.first(),
            bis_necklace=Gear.objects.first(),
            bis_offhand=Gear.objects.first(),
            bis_right_ring=Gear.objects.first(),
            current_body=Gear.objects.last(),
            current_bracelet=Gear.objects.last(),
            current_earrings=Gear.objects.last(),
            current_feet=Gear.objects.last(),
            current_hands=Gear.objects.last(),
            current_head=Gear.objects.last(),
            current_left_ring=Gear.objects.last(),
            current_legs=Gear.objects.last(),
            current_mainhand=Gear.objects.last(),
            current_necklace=Gear.objects.last(),
            current_offhand=Gear.objects.last(),
            current_right_ring=Gear.objects.last(),
            job=Job.objects.get(pk='DRG'),
            owner=char,
        )
        data = {
            'character_id': self.char.id,
            'bis_list_id': bis.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.content)
        content = response.json()
        self.assertEqual(content['character_id'], ['Please select a valid, verified Character that you own.'])
        self.assertEqual(content['bis_list_id'], ['Please select a valid BISList belonging to your Character.'])

        # Make the character a member of the team
        tm = TeamMember.objects.create(team=self.team, character=self.char, bis_list=self.bis)
        self.char.verified = True
        self.char.save()
        data = {
            'character_id': self.char.id,
            'bis_list_id': bis.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.content)
        content = response.json()
        self.assertEqual(content['character_id'], ['This Character is already a member of the Team.'])

        # Lastly check the top level validate error
        tm.delete()
        char.user = self._get_user()
        char.save()
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.content)
        content = response.json()
        self.assertEqual(content['bis_list_id'], ['Please select a valid BISList belonging to your Character.'])

    def test_404(self):
        """
        Test 404 errors for invalid invite urls
        """
        user = self._get_user()
        self.client.force_authenticate(user)
        url = reverse('api:team_invite', kwargs={'invite_code': 'abcde' * 8})

        self.assertEqual(self.client.head(url).status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(self.client.get(url).status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(self.client.post(url).status_code, status.HTTP_404_NOT_FOUND)
