from io import StringIO
from django.core.management import call_command
from django.urls import reverse
from rest_framework import status
from api.models import BISList, Character, Gear, Notification, Team, Tier
from api.serializers import TeamMemberSerializer
from .test_base import SavageAimTestCase


class TeamProxyCollection(SavageAimTestCase):
    """
    Tests related to Team Proxy creation
    """

    def setUp(self):
        """
        Prepopulate the DB with known data we can calculate off of
        """
        self.maxDiff = None
        call_command('all_seed', stdout=StringIO())

        # Create a Team first
        self.team = Team.objects.create(
            invite_code=Team.generate_invite_code(),
            name='Les Jambons',
            tier=Tier.objects.get(max_item_level=605),
        )

        # Create a Team lead to use to create a proxy character
        self.char = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=self._get_user(),
            name='Team Lead',
            verified=True,
            world='Lich',
        )
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

        # Lastly, link the characters to the team
        self.tm = self.team.members.create(character=self.char, bis_list=self.tl_main_bis, lead=True)

        # Map gear names to ids for ease
        self.gear_id_map = {g.name: g.id for g in Gear.objects.all()}

    def test_create(self):
        """
        Using the lead character, attempt to create a new proxy in the Team
        """
        url = reverse('api:team_proxy_collection', kwargs={'team_id': self.team.pk})
        user = self._get_user()
        self.client.force_authenticate(user)

        # Compile an object that combines a valid character and bis list request into one, and send it
        data = {
            'character': {
                'avatar_url': 'https://img.savageaim.com/test123',
                'lodestone_id': '3412557245',
                'name': 'New Proxy',
                'world': 'Zodiark (Light)',
            },
            'bis': {
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
            },
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        proxy_id = response.json()['id']

        # Also send a request to Team Read to ensure that the proxy character is returned
        url = reverse('api:team_resource', kwargs={'pk': self.team.id})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        content = response.json()
        self.assertEqual(len(content['members']), 2)

        # Ensure the BIS List has the Job name as the name
        self.assertEqual(content['members'][0]['character']['id'], proxy_id)
        self.assertEqual(content['members'][0]['bis_list']['display_name'], 'Paladin')

    def test_create_400(self):
        """
        Do some form of testing to make sure errors are reported properly from this view.
        Actual Character/BIS errors are tested elsewhere so we just need to see if they get returned here at all
        """
        url = reverse('api:team_proxy_collection', kwargs={'team_id': self.team.pk})
        user = self._get_user()
        self.client.force_authenticate(user)

        # Test sending nothing, ensure both dicts are full
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(len(response.json()['character']) > 0)
        self.assertTrue(len(response.json()['bis']) > 0)

        # Test sending valid character data and no bis data
        data = {
            'character': {
                'avatar_url': 'https://img.savageaim.com/test123',
                'lodestone_id': '3412557245',
                'name': 'New Proxy',
                'world': 'Zodiark (Light)',
            },
            'bis': {},
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.json()['character']), 0, response.json()['character'])
        self.assertTrue(len(response.json()['bis']) > 0)

        data = {
            'character': {},
            'bis': {
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
            },
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.json()['bis']), 0, response.json()['bis'])
        self.assertTrue(len(response.json()['character']) > 0)

    def test_404(self):
        """
        Test the cases that cause a 404 to be returned;

        - ID doesn't exist
        - Request from someone who doesn't have a character in the Team
        - Update request from someone who doesn't have a character in the Team
        - Update request from someone that isn't the team lead
        """
        user = self._get_user()
        self.client.force_authenticate(user)

        # ID doesn't exist
        url = reverse('api:team_proxy_collection', kwargs={'team_id': 'abcde-abcde-abcde-abcde'})
        response = self.client.post(url)

        url = reverse('api:team_proxy_collection', kwargs={'team_id': self.team.id})
        # Check update as non-team lead
        self.tm.lead = False
        self.tm.save()
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.content)

        # Delete membership altogether and test both read and update
        self.tm.delete()
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.content)
