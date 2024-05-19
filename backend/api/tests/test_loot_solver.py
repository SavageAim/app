from datetime import datetime, timedelta
from io import StringIO
from django.core.management import call_command
from django.urls import reverse
from rest_framework import status
from api.models import BISList, Character, Gear, Loot, Notification, Team, TeamMember, Tier
from api.views import LootSolver
from .test_base import SavageAimTestCase


class LootTestSuite(SavageAimTestCase):
    """
    Get a list of Tiers and make sure the correct list is returned
    """

    def setUp(self):
        """
        Prepopulate the DB with known data we can calculate off of
        """
        self.maxDiff = None
        call_command('seed', stdout=StringIO())

    def tearDown(self):
        """
        Clean up the DB after each test
        """
        Notification.objects.all().delete()
        Loot.objects.all().delete()
        TeamMember.objects.all().delete()
        Team.objects.all().delete()
        BISList.objects.all().delete()
        Character.objects.all().delete()

    def test_requirements_map_generation(self):
        """
        Build up a full test team, and run the requirements map function separately to ensure it builds the map correctly.
        """
        team = Team.objects.create(
            invite_code=Team.generate_invite_code(),
            name='The Testers',
            tier=Tier.objects.get(max_item_level=665),
        )
        raid_weapon = Gear.objects.get(item_level=665, name='Ascension')
        raid_gear = Gear.objects.get(item_level=660, name='Ascension')
        tome_gear = Gear.objects.get(name='Augmented Credendum')
        base_tome_gear = Gear.objects.get(name='Credendum')
        crafted_gear = Gear.objects.get(name='Diadochos')

        # Make an ease of use map for current stuff to avoid redefining it over and over
        current_map = {
            'current_mainhand': crafted_gear,
            'current_offhand': crafted_gear,
            'current_head': crafted_gear,
            'current_body': crafted_gear,
            'current_hands': crafted_gear,
            'current_legs': crafted_gear,
            'current_feet': crafted_gear,
            'current_earrings': crafted_gear,
            'current_necklace': crafted_gear,
            'current_bracelet': crafted_gear,
            'current_right_ring': crafted_gear,
            'current_left_ring': crafted_gear,
        }

        # Make 8 Characters that represent the team members
        c1 = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=self._get_user(),
            name='C1',
            verified=True,
            world='Lich',
        )
        c2 = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=self._get_user(),
            name='C2',
            verified=True,
            world='Lich',
        )
        c3 = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=self._get_user(),
            name='C3',
            verified=True,
            world='Lich',
        )
        c4 = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=self._get_user(),
            name='C4',
            verified=True,
            world='Lich',
        )
        c5 = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=self._get_user(),
            name='C5',
            verified=True,
            world='Lich',
        )
        c6 = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=self._get_user(),
            name='C6',
            verified=True,
            world='Lich',
        )
        c7 = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=self._get_user(),
            name='C7',
            verified=True,
            world='Lich',
        )
        c8 = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=self._get_user(),
            name='C8',
            verified=True,
            world='Lich',
        )

        # Next make 8 BIS Lists, one for each, and link em to the team
        b1 = BISList.objects.create(
            owner=c1,
            job_id='WAR',
            bis_mainhand=raid_weapon,
            bis_offhand=raid_weapon,
            bis_head=raid_gear,
            bis_body=tome_gear,
            bis_hands=raid_gear,
            bis_legs=raid_gear,
            bis_feet=tome_gear,
            bis_earrings=tome_gear,
            bis_necklace=raid_gear,
            bis_bracelet=tome_gear,
            bis_right_ring=tome_gear,
            bis_left_ring=base_tome_gear,
            **current_map,
        )
        team.members.create(character=c1, bis_list=b1, permissions=0)

        b2 = BISList.objects.create(
            owner=c2,
            job_id='DRK',
            bis_mainhand=raid_weapon,
            bis_offhand=raid_weapon,
            bis_head=raid_gear,
            bis_body=tome_gear,
            bis_hands=raid_gear,
            bis_legs=raid_gear,
            bis_feet=tome_gear,
            bis_earrings=tome_gear,
            bis_necklace=raid_gear,
            bis_bracelet=tome_gear,
            bis_right_ring=tome_gear,
            bis_left_ring=base_tome_gear,
            **current_map,
        )
        team.members.create(character=c2, bis_list=b2, permissions=0)

        b3 = BISList.objects.create(
            owner=c3,
            job_id='AST',
            bis_mainhand=raid_weapon,
            bis_offhand=raid_weapon,
            bis_head=raid_gear,
            bis_body=raid_gear,
            bis_hands=tome_gear,
            bis_legs=tome_gear,
            bis_feet=raid_gear,
            bis_earrings=tome_gear,
            bis_necklace=raid_gear,
            bis_bracelet=raid_gear,
            bis_right_ring=tome_gear,
            bis_left_ring=base_tome_gear,
            **current_map,
        )
        team.members.create(character=c3, bis_list=b3, lead=True)

        b4 = BISList.objects.create(
            owner=c4,
            job_id='SGE',
            bis_mainhand=raid_weapon,
            bis_offhand=raid_weapon,
            bis_head=tome_gear,
            bis_body=raid_gear,
            bis_hands=tome_gear,
            bis_legs=tome_gear,
            bis_feet=raid_gear,
            bis_earrings=tome_gear,
            bis_necklace=raid_gear,
            bis_bracelet=raid_gear,
            bis_right_ring=tome_gear,
            bis_left_ring=base_tome_gear,
            **current_map,
        )
        team.members.create(character=c4, bis_list=b4, permissions=0)

        b5 = BISList.objects.create(
            owner=c5,
            job_id='MNK',
            bis_mainhand=raid_weapon,
            bis_offhand=raid_weapon,
            bis_head=raid_gear,
            bis_body=raid_gear,
            bis_hands=tome_gear,
            bis_legs=tome_gear,
            bis_feet=raid_gear,
            bis_earrings=raid_gear,
            bis_necklace=tome_gear,
            bis_bracelet=raid_gear,
            bis_right_ring=raid_gear,
            bis_left_ring=tome_gear,
            **current_map,
        )
        team.members.create(character=c5, bis_list=b5, permissions=0)

        b6 = BISList.objects.create(
            owner=c6,
            job_id='RPR',
            bis_mainhand=raid_weapon,
            bis_offhand=raid_weapon,
            bis_head=tome_gear,
            bis_body=raid_gear,
            bis_hands=tome_gear,
            bis_legs=tome_gear,
            bis_feet=raid_gear,
            bis_earrings=raid_gear,
            bis_necklace=tome_gear,
            bis_bracelet=raid_gear,
            bis_right_ring=tome_gear,
            bis_left_ring=raid_gear,
            **current_map,
        )
        team.members.create(character=c6, bis_list=b6, permissions=0)

        b7 = BISList.objects.create(
            owner=c7,
            job_id='BRD',
            bis_mainhand=raid_weapon,
            bis_offhand=raid_weapon,
            bis_head=raid_gear,
            bis_body=tome_gear,
            bis_hands=raid_gear,
            bis_legs=raid_gear,
            bis_feet=tome_gear,
            bis_earrings=tome_gear,
            bis_necklace=raid_gear,
            bis_bracelet=tome_gear,
            bis_right_ring=tome_gear,
            bis_left_ring=raid_gear,
            **current_map,
        )
        team.members.create(character=c7, bis_list=b7, permissions=0)

        b8 = BISList.objects.create(
            owner=c8,
            job_id='BLM',
            bis_mainhand=raid_weapon,
            bis_offhand=raid_weapon,
            bis_head=raid_gear,
            bis_body=raid_gear,
            bis_hands=tome_gear,
            bis_legs=tome_gear,
            bis_feet=raid_gear,
            bis_earrings=tome_gear,
            bis_necklace=raid_gear,
            bis_bracelet=tome_gear,
            bis_right_ring=tome_gear,
            bis_left_ring=raid_gear,
            **current_map,
        )
        team.members.create(character=c8, bis_list=b8, permissions=0)

        # Generate the expected map
        expected = {
            'earrings': [c5.id, c6.id],
            'necklace': [c1.id, c2.id, c3.id, c4.id, c7.id, c8.id],
            'bracelet': [c3.id, c4.id, c5.id, c6.id],
            'ring': [c5.id, c6.id, c7.id, c8.id],
            'head': [c1.id, c2.id, c3.id, c5.id, c7.id, c8.id],
            'hands': [c1.id, c2.id, c7.id],
            'feet': [c3.id, c4.id, c5.id, c6.id, c8.id],
            'tome-accessory-augment': [c1.id, c1.id, c1.id, c2.id, c2.id, c2.id, c3.id, c3.id, c4.id, c4.id, c5.id, c5.id, c6.id, c6.id, c7.id, c7.id, c7.id, c8.id, c8.id, c8.id],
            'body': [c3.id, c4.id, c5.id, c6.id, c8.id],
            'legs': [c1.id, c2.id, c7.id],
            'tome-armour-augment': [c1.id, c1.id, c2.id, c2.id, c3.id, c3.id, c4.id, c4.id, c4.id, c5.id, c5.id, c6.id, c6.id, c6.id, c7.id, c7.id, c8.id, c8.id]
        }

        self.maxDiff = None
        received = LootSolver._get_requirements_map(team)
        for slot in expected:
            self.assertEqual(expected[slot], received[slot], slot)

        # Now give some people BIS items and ensure the requirements map updates accordingly
        b1.current_head = raid_gear
        b1.current_feet = tome_gear
        b1.current_earrings = tome_gear
        b1.save()
        expected['head'].remove(c1.id)
        expected['tome-armour-augment'].remove(c1.id)
        expected['tome-accessory-augment'].remove(c1.id)

    def test_prio_bracket_generation(self):
        """
        Create some test maps as subsets of the expected data from the last test, and get the expected priority brackets generated
        """
        first_floor_requirements = {
            'earrings': [5, 6],
            'necklace': [1, 2, 3, 4, 7, 8],
            'bracelet': [3, 4, 5, 6],
            'ring': [5, 6, 7, 8],
        }
        second_floor_requirements = {
            'head': [1, 2, 3, 5, 7, 8],
            'hands': [1, 2, 7],
            'feet': [3, 4, 5, 6, 8],
            'tome-accessory-augment': [1, 1, 1, 2, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 7, 8, 8, 8],
        }
        third_floor_requirements = {
            'body': [3, 4, 5, 6, 8],
            'legs': [1, 2, 7],
            'tome-armour-augment': [1, 1, 2, 2, 3, 3, 4, 4, 4, 5, 5, 6, 6, 6, 7, 7, 8, 8]
        }
        ordering = [5, 6, 7, 8, 1, 2, 3, 4]

        first_floor_expected = {
            3: [5, 6],
            2: [7, 8, 3, 4],
            1: [1, 2],
        }
        second_floor_expected = {
            5: [7, 8, 1, 2],
            4: [5, 3],
            3: [6, 4],
        }
        third_floor_expected = {
            4: [6, 4],
            3: [5, 7, 8, 1, 2, 3],
        }

        self.assertDictEqual(LootSolver._generate_priority_brackets(first_floor_requirements, ordering), first_floor_expected)
        self.assertDictEqual(LootSolver._generate_priority_brackets(second_floor_requirements, ordering), second_floor_expected)
        self.assertDictEqual(LootSolver._generate_priority_brackets(third_floor_requirements, ordering), third_floor_expected)

    def test_clear_count_calculator(self):
        """
        Test that the clear count calculator is correct
        """
        team = Team.objects.create(
            invite_code=Team.generate_invite_code(),
            name='The Testers',
            tier=Tier.objects.get(max_item_level=665),
        )
        tier = Tier.objects.get(max_item_level=665)
        clears, _ = LootSolver._get_floor_prio_and_clear_count({}, Loot.objects.all(), {'earrings', 'necklace', 'bracelet', 'ring'})
        self.assertEqual(clears, 0)
        Loot.objects.create(
            item='ring',
            obtained='2024-01-01',
            team=team,
            tier=tier,
        )
        Loot.objects.create(
            item='earrings',
            obtained='2024-01-01',
            team=team,
            tier=tier,
        )
        Loot.objects.create(
            item='ring',
            obtained='2024-01-02',
            team=team,
            tier=tier,
            greed=True,
        )
        Loot.objects.create(
            item='head',
            obtained='2024-01-03',
            team=team,
            tier=tier,
        )

        clears, _ = LootSolver._get_floor_prio_and_clear_count({}, Loot.objects.all(), {'earrings', 'necklace', 'bracelet', 'ring'})
        self.assertEqual(clears, 2)
