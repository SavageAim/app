from datetime import datetime
from io import StringIO
from django.core.management import call_command
from api import models
from .test_base import SavageAimTestCase

__all__ = ['ManagementCommandTestSuite']


class ManagementCommandTestSuite(SavageAimTestCase):

    def test_integrity(self):
        """
        Seed the DB and ensure seeded data maintains integrity in various ways;

        - Any gear names mentioned by Tiers should exist
        - Any item levels mentioned by Tiers should exist
        - Ordering numbers should be unique per role
        """
        call_command('seed', stdout=StringIO())

        for tier in models.Tier.objects.all():
            self.assertTrue(
                models.Gear.objects.filter(item_level=tier.max_item_level).exists(),
                f'Found no Gear of item level {tier.max_item_level} for Tier "{tier.name}".',
            )
            self.assertTrue(
                models.Gear.objects.filter(name=tier.tome_gear_name).exists(),
                f'"{tier.tome_gear_name}" is not a valid Gear name for Tier "{tier.name}".',
            )
            self.assertTrue(
                models.Gear.objects.filter(name=tier.raid_gear_name).exists(),
                f'"{tier.raid_gear_name}" is not a valid Gear name for Tier "{tier.name}".',
            )

        # Get ordering values from DB
        cap = models.Job.objects.order_by('-ordering').first().ordering
        for value in range(cap + 1):
            roles = models.Job.objects.filter(ordering=value).values_list('role', flat=True)
            expected = len(set(roles))
            self.assertEqual(
                len(roles),
                expected,
                f'Found {len(roles)} Jobs with ordering {value}, expected {expected}.\n\t'
                f'Found {list(roles)} expected {list(set(roles))}.',
            )

    def test_loot_team_link(self):
        """
        Create a Loot object with team=None, run the command and ensure the correct team was created
        """
        call_command('seed', stdout=StringIO())

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
            name='Team Lead',
            verified=True,
            world='Lich',
        )

        # Next, create two BIS lists for each character
        raid_weapon = models.Gear.objects.get(item_level=605, name='Asphodelos')
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

    def test_save_bis_list_ring_swap(self):
        """
        Create a BISList with rings swapped, then run the management command
        """
        call_command('seed', stdout=StringIO())
        char = models.Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=self._get_user(),
            name='Team Lead',
            verified=True,
            world='Lich',
        )

        # Next, create two BIS lists for each character
        raid_weapon = models.Gear.objects.get(item_level=605, name='Asphodelos')
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
            bis_legs=tome_gear,
            bis_mainhand=raid_weapon,
            bis_necklace=tome_gear,
            bis_offhand=raid_weapon,
            bis_left_ring=tome_gear,
            bis_right_ring=raid_gear,
            current_body=crafted,
            current_bracelet=crafted,
            current_earrings=crafted,
            current_feet=crafted,
            current_hands=crafted,
            current_head=crafted,
            current_legs=crafted,
            current_mainhand=crafted,
            current_necklace=crafted,
            current_offhand=crafted,
            current_left_ring=crafted,
            current_right_ring=tome_gear,
            job_id='SGE',
            owner=char,
        )
        models.BISList.objects.update(
            current_right_ring_id=tome_gear.id,
            current_left_ring_id=crafted.id,
        )
        bis.refresh_from_db()
        self.assertNotEqual(bis.current_right_ring_id, crafted.id)
        self.assertNotEqual(bis.current_left_ring_id, tome_gear.id)
        call_command('save_all_bis_lists')
        bis.refresh_from_db()
        self.assertEqual(bis.current_right_ring_id, crafted.id)
        self.assertEqual(bis.current_left_ring_id, tome_gear.id)
