from datetime import datetime
from io import StringIO
from django.core.management import call_command
from api import models
from .test_base import SavageAimTestCase

__all__ = ['ManagementCommandTestSuite']


class ManagementCommandTestSuite(SavageAimTestCase):

    def test_gear_seed(self):
        """
        Run the gear seed command and check that it works as intended

        May need to change numbers as the command gets more gear
        """
        call_command('gear_seed', stdout=StringIO())

        self.assertTrue(models.Gear.objects.exists())
        self.assertEqual(models.Gear.objects.filter(item_level=560).count(), 2)
        self.assertEqual(models.Gear.objects.filter(item_level=580).count(), 4)

    def test_job_seed(self):
        """
        Run the job seed command and ensure everything is as it should be
        """
        call_command('job_seed', stdout=StringIO())

        # Test search order matches what's expected
        order = [
            'PLD',
            'WAR',
            'DRK',
            'GNB',
            'WHM',
            'SCH',
            'AST',
            'SGE',
            'MNK',
            'DRG',
            'NIN',
            'SAM',
            'RPR',
            'BRD',
            'MCH',
            'DNC',
            'BLM',
            'SMN',
            'RDM',
        ]

        data = models.Job.objects.all()

        for i in range(len(order)):
            self.assertEqual(data[i].id, order[i])

    def test_loot_team_link(self):
        """
        Create a Loot object with team=None, run the command and ensure the correct team was created
        """
        call_command('tier_seed', stdout=StringIO())
        call_command('gear_seed', stdout=StringIO())
        call_command('job_seed', stdout=StringIO())

        # Create a Team first
        team = models.Team.objects.create(
            invite_code=models.Team.generate_invite_code(),
            name='Les Jambons',
            tier=models.Tier.objects.get(max_item_level=605),
        )

        # Create two characters belonging to separate users
        char = models.Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=self._get_user(),
            name='Raid Lead',
            verified=True,
            world='Lich',
        )

        # Next, create two BIS lists for each character
        raid_weapon = models.Gear.objects.get(item_level=605)
        raid_gear = models.Gear.objects.get(item_level=600, has_weapon=False)
        tome_gear = models.Gear.objects.get(item_level=600, has_weapon=True)
        crafted = models.Gear.objects.get(name='Classical')
        bis = models.BISList.objects.create(
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
            owner=char,
        )

        # Lastly, link the characters to the team
        tm = team.members.create(character=char, bis_list=bis, lead=True)

        # Create a Loot object without the team value
        loot = models.Loot.objects.create(
            obtained=datetime.today(),
            member=tm,
            greed=False,
            item='mount',
            tier=team.tier,
            team=None,
        )
        self.assertIsNone(loot.team)

        call_command('loot_team_link', stdout=StringIO())
        loot.refresh_from_db()
        self.assertEqual(loot.team, team)

    def test_notification_setup(self):
        """
        Set up a User, run the command and ensure that the keys are present and set to True
        Add a key with False before running the command to ensure that hasn't been affected
        """
        user = self._create_user()
        settings = models.Settings.objects.create(user=user, notifications={'verify_fail': False})
        call_command('notification_setup')
        settings.refresh_from_db()
        self.assertTrue('verify_success' in settings.notifications)
        self.assertTrue(settings.notifications['verify_success'])
        self.assertFalse(settings.notifications['verify_fail'])

    def test_tier_seed(self):
        """
        Run the tier seed command and check that it works as intended

        May need to change numbers as the command gets more tiers
        """
        call_command('tier_seed', stdout=StringIO())

        self.assertTrue(models.Tier.objects.exists())
        self.assertEqual(models.Tier.objects.count(), 1)
        self.assertEqual(models.Tier.objects.first().max_item_level, 605)  # Asphodelos
