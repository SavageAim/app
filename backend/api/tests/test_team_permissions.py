# stdlib
from io import StringIO
from random import randint
# lib
from django.core.management import call_command
from django.urls import reverse
from rest_framework import status
# local
from api.models import BISList, Character, Gear, Notification, Job, Team, TeamMember, TeamMemberPermissions, Tier
from api.serializers import TeamSerializer
from .test_base import SavageAimTestCase


class TeamPermissions(SavageAimTestCase):
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

    def tearDown(self):
        """
        Clean up the DB after each test
        """
        TeamMember.objects.all().delete()
        Team.objects.all().delete()
        BISList.objects.all().delete()
        Character.objects.all().delete()

    def _create_member(self, team: Team):
        """
        Create a character with a BIS List to be used for the team member
        """
        char = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=randint(1000, 1000000),
            user=self._create_user(),
            name=f'Char {randint(0, 100)}',
            world='Lich',
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
        return team.members.create(character=char, bis_list=bis)

    def test_permissions(self):
        """
        Create some members for a Team, and then test their permissions
        """
        url = reverse('api:team_collection')

        # Create a Team and add three members
        team = Team.objects.create(
            invite_code=Team.generate_invite_code(),
            name='Test Team',
            tier=Tier.objects.first(),
        )
        member1 = self._create_member(team)
        member2 = self._create_member(team)
        member3 = self._create_member(team)

        # Log in as the leader
        member1.lead = True
        member1.save()
        self.client.force_authenticate(member1.character.user)
