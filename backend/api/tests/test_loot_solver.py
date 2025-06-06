from io import StringIO
from django.core.management import call_command
from django.urls import reverse
from rest_framework import status
from api.models import BISList, Character, Gear, Loot, Notification, Team, TeamMember, Tier
from api.views import LootSolver
from .test_base import SavageAimTestCase


class LootSolverTestSuite(SavageAimTestCase):
    """
    Test the LootSolver's functionality
    """

    def setUp(self):
        """
        Seed the DB
        """
        self.maxDiff = None
        call_command('seed', stdout=StringIO())

        self.tier = Tier.objects.get(max_item_level=665)
        self.team = Team.objects.create(
            invite_code=Team.generate_invite_code(),
            name='The Testers',
            tier=self.tier,
        )
        self.raid_weapon = Gear.objects.get(item_level=665, name='Ascension')
        self.raid_gear = Gear.objects.get(item_level=660, name='Ascension')
        self.tome_gear = Gear.objects.get(name='Augmented Credendum')
        self.base_tome_gear = Gear.objects.get(name='Credendum')
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
        self.c1 = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=self._get_user(),
            name='C1',
            verified=True,
            world='Lich',
        )
        self.c2 = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=self._get_user(),
            name='C2',
            verified=True,
            world='Lich',
        )
        self.c3 = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=self._get_user(),
            name='C3',
            verified=True,
            world='Lich',
        )
        self.c4 = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=self._get_user(),
            name='C4',
            verified=True,
            world='Lich',
        )
        self.c5 = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=self._get_user(),
            name='C5',
            verified=True,
            world='Lich',
        )
        self.c6 = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=self._get_user(),
            name='C6',
            verified=True,
            world='Lich',
        )
        self.c7 = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=self._get_user(),
            name='C7',
            verified=True,
            world='Lich',
        )
        self.c8 = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=self._get_user(),
            name='C8',
            verified=True,
            world='Lich',
        )

        # Next make 8 BIS Lists, one for each, and link em to the team
        self.b1 = BISList.objects.create(
            owner=self.c1,
            job_id='WAR',
            bis_mainhand=self.raid_weapon,
            bis_offhand=self.raid_weapon,
            bis_head=self.raid_gear,
            bis_body=self.tome_gear,
            bis_hands=self.raid_gear,
            bis_legs=self.raid_gear,
            bis_feet=self.tome_gear,
            bis_earrings=self.tome_gear,
            bis_necklace=self.raid_gear,
            bis_bracelet=self.tome_gear,
            bis_right_ring=self.tome_gear,
            bis_left_ring=self.base_tome_gear,
            **current_map,
        )
        self.tm1 = self.team.members.create(character=self.c1, bis_list=self.b1, permissions=0)

        self.b2 = BISList.objects.create(
            owner=self.c2,
            job_id='DRK',
            bis_mainhand=self.raid_weapon,
            bis_offhand=self.raid_weapon,
            bis_head=self.raid_gear,
            bis_body=self.tome_gear,
            bis_hands=self.raid_gear,
            bis_legs=self.raid_gear,
            bis_feet=self.tome_gear,
            bis_earrings=self.tome_gear,
            bis_necklace=self.raid_gear,
            bis_bracelet=self.tome_gear,
            bis_right_ring=self.tome_gear,
            bis_left_ring=self.base_tome_gear,
            **current_map,
        )
        self.tm2 = self.team.members.create(character=self.c2, bis_list=self.b2, permissions=0)

        self.b3 = BISList.objects.create(
            owner=self.c3,
            job_id='AST',
            bis_mainhand=self.raid_weapon,
            bis_offhand=self.raid_weapon,
            bis_head=self.raid_gear,
            bis_body=self.raid_gear,
            bis_hands=self.tome_gear,
            bis_legs=self.tome_gear,
            bis_feet=self.raid_gear,
            bis_earrings=self.tome_gear,
            bis_necklace=self.raid_gear,
            bis_bracelet=self.raid_gear,
            bis_right_ring=self.tome_gear,
            bis_left_ring=self.base_tome_gear,
            **current_map,
        )
        self.tm3 = self.team.members.create(character=self.c3, bis_list=self.b3, lead=True)

        self.b4 = BISList.objects.create(
            owner=self.c4,
            job_id='SGE',
            bis_mainhand=self.raid_weapon,
            bis_offhand=self.raid_weapon,
            bis_head=self.tome_gear,
            bis_body=self.raid_gear,
            bis_hands=self.tome_gear,
            bis_legs=self.tome_gear,
            bis_feet=self.raid_gear,
            bis_earrings=self.tome_gear,
            bis_necklace=self.raid_gear,
            bis_bracelet=self.raid_gear,
            bis_right_ring=self.tome_gear,
            bis_left_ring=self.base_tome_gear,
            **current_map,
        )
        self.tm4 = self.team.members.create(character=self.c4, bis_list=self.b4, permissions=0)

        self.b5 = BISList.objects.create(
            owner=self.c5,
            job_id='MNK',
            bis_mainhand=self.raid_weapon,
            bis_offhand=self.raid_weapon,
            bis_head=self.raid_gear,
            bis_body=self.raid_gear,
            bis_hands=self.tome_gear,
            bis_legs=self.tome_gear,
            bis_feet=self.raid_gear,
            bis_earrings=self.raid_gear,
            bis_necklace=self.tome_gear,
            bis_bracelet=self.raid_gear,
            bis_right_ring=self.raid_gear,
            bis_left_ring=self.tome_gear,
            **current_map,
        )
        self.tm5 = self.team.members.create(character=self.c5, bis_list=self.b5, permissions=0)

        self.b6 = BISList.objects.create(
            owner=self.c6,
            job_id='RPR',
            bis_mainhand=self.raid_weapon,
            bis_offhand=self.raid_weapon,
            bis_head=self.tome_gear,
            bis_body=self.raid_gear,
            bis_hands=self.tome_gear,
            bis_legs=self.tome_gear,
            bis_feet=self.raid_gear,
            bis_earrings=self.raid_gear,
            bis_necklace=self.tome_gear,
            bis_bracelet=self.raid_gear,
            bis_right_ring=self.tome_gear,
            bis_left_ring=self.raid_gear,
            **current_map,
        )
        self.tm6 = self.team.members.create(character=self.c6, bis_list=self.b6, permissions=0)

        self.b7 = BISList.objects.create(
            owner=self.c7,
            job_id='BRD',
            bis_mainhand=self.raid_weapon,
            bis_offhand=self.raid_weapon,
            bis_head=self.raid_gear,
            bis_body=self.tome_gear,
            bis_hands=self.raid_gear,
            bis_legs=self.raid_gear,
            bis_feet=self.tome_gear,
            bis_earrings=self.tome_gear,
            bis_necklace=self.raid_gear,
            bis_bracelet=self.tome_gear,
            bis_right_ring=self.tome_gear,
            bis_left_ring=self.raid_gear,
            **current_map,
        )
        self.tm7 = self.team.members.create(character=self.c7, bis_list=self.b7, permissions=0)

        self.b8 = BISList.objects.create(
            owner=self.c8,
            job_id='BLM',
            bis_mainhand=self.raid_weapon,
            bis_offhand=self.raid_weapon,
            bis_head=self.raid_gear,
            bis_body=self.raid_gear,
            bis_hands=self.tome_gear,
            bis_legs=self.tome_gear,
            bis_feet=self.raid_gear,
            bis_earrings=self.tome_gear,
            bis_necklace=self.raid_gear,
            bis_bracelet=self.tome_gear,
            bis_right_ring=self.tome_gear,
            bis_left_ring=self.raid_gear,
            **current_map,
        )
        self.tm8 = self.team.members.create(character=self.c8, bis_list=self.b8, permissions=0)

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

    # def test_list(self):
    #     from django.conf import settings
    #     from django.db import connection, reset_queries

    #     settings.DEBUG = True
    #     reset_queries()

    #     # Run a list as the user
    #     url = reverse('api:team_collection')
    #     user = self._get_user()
    #     self.client.force_authenticate(user)
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)

    #     print(len(connection.queries))

    def test_requirements_map_generation(self):
        """
        Build up a full test team, and run the requirements map function separately to ensure it builds the map correctly.
        """
        # Generate the expected map
        expected = {
            'earrings': [self.tm5.id, self.tm6.id],
            'necklace': [self.tm1.id, self.tm2.id, self.tm3.id, self.tm4.id, self.tm7.id, self.tm8.id],
            'bracelet': [self.tm3.id, self.tm4.id, self.tm5.id, self.tm6.id],
            'ring': [self.tm5.id, self.tm6.id, self.tm7.id, self.tm8.id],
            'head': [self.tm1.id, self.tm2.id, self.tm3.id, self.tm5.id, self.tm7.id, self.tm8.id],
            'hands': [self.tm1.id, self.tm2.id, self.tm7.id],
            'feet': [self.tm3.id, self.tm4.id, self.tm5.id, self.tm6.id, self.tm8.id],
            'tome-accessory-augment': [self.tm1.id, self.tm1.id, self.tm1.id, self.tm2.id, self.tm2.id, self.tm2.id, self.tm3.id, self.tm3.id, self.tm4.id, self.tm4.id, self.tm5.id, self.tm5.id, self.tm6.id, self.tm6.id, self.tm7.id, self.tm7.id, self.tm7.id, self.tm8.id, self.tm8.id, self.tm8.id],
            'body': [self.tm3.id, self.tm4.id, self.tm5.id, self.tm6.id, self.tm8.id],
            'legs': [self.tm1.id, self.tm2.id, self.tm7.id],
            'tome-armour-augment': [self.tm1.id, self.tm1.id, self.tm2.id, self.tm2.id, self.tm3.id, self.tm3.id, self.tm4.id, self.tm4.id, self.tm4.id, self.tm5.id, self.tm5.id, self.tm6.id, self.tm6.id, self.tm6.id, self.tm7.id, self.tm7.id, self.tm8.id, self.tm8.id],
            'mainhand': [self.tm1.id, self.tm2.id, self.tm3.id, self.tm4.id, self.tm5.id, self.tm6.id, self.tm7.id, self.tm8.id],
        }

        received = dict(LootSolver._get_requirements_map(self.team))
        self.assertDictEqual(expected, received)

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
        clears, *_ = LootSolver._get_floor_data({}, Loot.objects.all(), {'earrings', 'necklace', 'bracelet', 'ring'}, [], {})
        self.assertEqual(clears, 0)
        Loot.objects.create(
            item='ring',
            obtained='2024-01-01',
            team=self.team,
            tier=self.tier,
        )
        Loot.objects.create(
            item='earrings',
            obtained='2024-01-01',
            team=self.team,
            tier=self.tier,
        )
        Loot.objects.create(
            item='ring',
            obtained='2024-01-02',
            team=self.team,
            tier=self.tier,
            greed=True,
        )
        Loot.objects.create(
            item='head',
            obtained='2024-01-03',
            team=self.team,
            tier=self.tier,
        )

        # Ensure that the floor prio generation also works as expected
        requirements = {
            'earrings': [5, 6],
            'necklace': [1, 2, 3, 4, 7, 8],
            'bracelet': [3, 4, 5, 6],
            'ring': [5, 6, 7, 8],
            'head': [2, 4, 8],
        }
        clears, prio_brackets, _ = LootSolver._get_floor_data(requirements, Loot.objects.all(), {'earrings', 'necklace', 'bracelet', 'ring'}, [5, 6, 7, 8, 1, 2, 3, 4], {})
        self.assertEqual(clears, 2)
        expected_brackets = {
            3: [5, 6],
            2: [7, 8, 3, 4],
            1: [1, 2],
        }
        self.assertDictEqual(prio_brackets, expected_brackets)

    def test_removing_obtained_requirements(self):
        """
        The _get_floor_data function also removes obtained items from the requirements map that is generated by the _get_requirements
        """

        # Second Floor Clear 1
        Loot.objects.create(
            item='head',
            member=self.tm3,
            tier=self.tier,
            team=self.team,
            obtained='2024-01-01',
        )
        self.b3.current_head = self.raid_gear
        self.b3.save()
        Loot.objects.create(
            item='hands',
            member=self.tm7,
            tier=self.tier,
            team=self.team,
            obtained='2024-01-01',
        )
        self.b7.current_hands = self.raid_gear
        self.b7.save()
        Loot.objects.create(
            item='feet',
            member=self.tm4,
            tier=self.tier,
            team=self.team,
            obtained='2024-01-01',
        )
        self.b4.current_feet = self.raid_gear
        self.b4.save()
        Loot.objects.create(
            item='tome-accessory-augment',
            member=self.tm6,
            tier=self.tier,
            team=self.team,
            obtained='2024-01-01',
        )
        self.b6.current_right_ring = self.tome_gear
        self.b6.save()
        # Second Floor Clear 2
        Loot.objects.create(
            item='head',
            member=self.tm2,
            tier=self.tier,
            team=self.team,
            obtained='2024-01-02',
        )
        self.b2.current_head = self.raid_gear
        self.b2.save()
        Loot.objects.create(
            item='hands',
            member=self.tm2,
            tier=self.tier,
            team=self.team,
            obtained='2024-01-02',
        )
        self.b2.current_hands = self.raid_gear
        self.b2.save()
        Loot.objects.create(
            item='feet',
            member=self.tm8,
            tier=self.tier,
            team=self.team,
            obtained='2024-01-02',
        )
        self.b8.current_feet = self.raid_gear
        self.b8.save()
        Loot.objects.create(
            item='tome-accessory-augment',
            member=self.tm7,
            tier=self.tier,
            team=self.team,
            obtained='2024-01-02',
        )
        self.b7.current_right_ring = self.tome_gear
        self.b7.save()

        # Generate the expected map
        expected = {
            'head': [self.tm1.id, self.tm5.id, self.tm7.id, self.tm8.id],
            'hands': [self.tm1.id],
            'feet': [self.tm3.id, self.tm5.id, self.tm6.id],
            'tome-accessory-augment': [self.tm1.id, self.tm1.id, self.tm1.id, self.tm2.id, self.tm2.id, self.tm2.id, self.tm3.id, self.tm3.id, self.tm4.id, self.tm4.id, self.tm5.id, self.tm5.id, self.tm6.id, self.tm7.id, self.tm7.id, self.tm8.id, self.tm8.id, self.tm8.id],
        }
        requirements = LootSolver._get_requirements_map(self.team)

        order = [self.tm5.id, self.tm6.id, self.tm7.id, self.tm8.id, self.tm1.id, self.tm2.id, self.tm3.id, self.tm4.id]
        *_, floor_current_requirements = LootSolver._get_floor_data(requirements, Loot.objects.all(), ['head', 'hands', 'feet', 'tome-accessory-augment'], order, {})
        self.assertDictEqual(floor_current_requirements, expected)

    def test_whole_view(self):
        """
        Generate the exact same team for the above tests but run the full view and get the information we need.
        Simulate some loot handouts in the team as well to make it a slightly different test case.
        """
        # First Floor Clear 1
        Loot.objects.create(
            item='necklace',
            member=self.tm4,
            tier=self.tier,
            team=self.team,
            obtained='2024-01-01',
        )
        self.b4.current_necklace = self.raid_gear
        self.b4.save()
        Loot.objects.create(
            item='bracelet',
            member=self.tm3,
            tier=self.tier,
            team=self.team,
            obtained='2024-01-01',
        )
        self.b3.current_bracelet = self.raid_gear
        self.b3.save()
        Loot.objects.create(
            item='ring',
            member=self.tm8,
            tier=self.tier,
            team=self.team,
            obtained='2024-01-01',
        )
        self.b8.current_left_ring = self.raid_gear
        self.b8.save()
        # Second Floor Clear 1
        Loot.objects.create(
            item='head',
            member=self.tm3,
            tier=self.tier,
            team=self.team,
            obtained='2024-01-01',
        )
        self.b3.current_head = self.raid_gear
        self.b3.save()
        Loot.objects.create(
            item='hands',
            member=self.tm7,
            tier=self.tier,
            team=self.team,
            obtained='2024-01-01',
        )
        self.b7.current_hands = self.raid_gear
        self.b7.save()
        Loot.objects.create(
            item='feet',
            member=self.tm4,
            tier=self.tier,
            team=self.team,
            obtained='2024-01-01',
        )
        self.b4.current_feet = self.raid_gear
        self.b4.save()
        Loot.objects.create(
            item='tome-accessory-augment',
            member=self.tm6,
            tier=self.tier,
            team=self.team,
            obtained='2024-01-01',
        )
        self.b6.current_right_ring = self.tome_gear
        self.b6.save()
        # Second Floor Clear 2
        Loot.objects.create(
            item='head',
            member=self.tm2,
            tier=self.tier,
            team=self.team,
            obtained='2024-01-02',
        )
        self.b2.current_head = self.raid_gear
        self.b2.save()
        Loot.objects.create(
            item='hands',
            member=self.tm2,
            tier=self.tier,
            team=self.team,
            obtained='2024-01-02',
        )
        self.b2.current_hands = self.raid_gear
        self.b2.save()
        Loot.objects.create(
            item='feet',
            member=self.tm8,
            tier=self.tier,
            team=self.team,
            obtained='2024-01-02',
        )
        self.b8.current_feet = self.raid_gear
        self.b8.save()
        Loot.objects.create(
            item='tome-accessory-augment',
            member=self.tm7,
            tier=self.tier,
            team=self.team,
            obtained='2024-01-02',
        )
        self.b7.current_right_ring = self.tome_gear
        self.b7.save()

        url = reverse('api:loot_solver', kwargs={'team_id': self.team.pk})
        user = self._get_user()
        self.client.force_authenticate(user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        content = response.json()

        first_floor_expected = [
            {'token': False, 'Earrings': self.tm5.id, 'Necklace': self.tm1.id, 'Bracelet': self.tm6.id, 'Ring': self.tm7.id},
            {'token': True, 'Earrings': self.tm6.id, 'Necklace': self.tm2.id, 'Bracelet': self.tm4.id, 'Ring': self.tm5.id},
        ]
        first_floor_received = content['first_floor']
        self.assertEqual(len(first_floor_expected), len(first_floor_received), first_floor_received)
        for i in range(len(first_floor_expected)):
            self.assertDictEqual(first_floor_expected[i], first_floor_received[i], f'{i+1}/{len(first_floor_received)}')

        second_floor_expected = [
            {'token': True, 'Head': self.tm5.id, 'Hands': self.tm1.id, 'Feet': self.tm3.id, 'Tome Accessory Augment': self.tm8.id},
            {'token': False, 'Head': self.tm1.id, 'Hands': None, 'Feet': self.tm5.id, 'Tome Accessory Augment': self.tm2.id},
            {'token': False, 'Head': self.tm7.id, 'Hands': None, 'Feet': self.tm6.id, 'Tome Accessory Augment': self.tm1.id},
            {'token': True, 'Head': self.tm8.id, 'Hands': None, 'Feet': None, 'Tome Accessory Augment': self.tm4.id},
        ]
        second_floor_received = content['second_floor']
        self.assertEqual(len(second_floor_expected), len(second_floor_received), second_floor_received)
        for i in range(len(second_floor_expected)):
            self.assertDictEqual(second_floor_expected[i], second_floor_received[i], f'{i+1}/{len(second_floor_received)}')

        third_floor_expected = [
            {'token': False, 'Body': self.tm6.id, 'Legs': self.tm7.id, 'Tome Armour Augment': self.tm4.id},
            {'token': False, 'Body': self.tm5.id, 'Legs': self.tm1.id, 'Tome Armour Augment': self.tm8.id},
            {'token': False, 'Body': self.tm3.id, 'Legs': self.tm2.id, 'Tome Armour Augment': self.tm6.id},
            {'token': True, 'Body': self.tm4.id, 'Legs': None, 'Tome Armour Augment': self.tm7.id},
            {'token': False, 'Body': self.tm8.id, 'Legs': None, 'Tome Armour Augment': self.tm1.id},
            {'token': False, 'Body': None, 'Legs': None, 'Tome Armour Augment': self.tm5.id},
            {'token': False, 'Body': None, 'Legs': None, 'Tome Armour Augment': self.tm6.id},
            {'token': True, 'Body': None, 'Legs': None, 'Tome Armour Augment': self.tm2.id},
        ]
        third_floor_received = content['third_floor']
        self.assertEqual(len(third_floor_expected), len(third_floor_received), third_floor_received)
        for i in range(len(third_floor_expected)):
            self.assertDictEqual(third_floor_expected[i], third_floor_received[i], f'{i+1}/{len(third_floor_received)}')

        self.assertEqual(content['fourth_floor'], {'weapons': 8, 'mounts': 8})

    def test_whole_view_split_loot(self):
        """
        Generate the exact same team for the above tests but run the full view and get the information we need.
        Simulate some loot handouts in the team as well to make it a slightly different test case.
        Give 2 clears worth of loot of Second Floor on the same day
        """
        # First Floor Clear 1
        Loot.objects.create(
            item='necklace',
            member=self.tm4,
            tier=self.tier,
            team=self.team,
            obtained='2024-01-01',
        )
        self.b4.current_necklace = self.raid_gear
        self.b4.save()
        Loot.objects.create(
            item='bracelet',
            member=self.tm3,
            tier=self.tier,
            team=self.team,
            obtained='2024-01-01',
        )
        self.b3.current_bracelet = self.raid_gear
        self.b3.save()
        Loot.objects.create(
            item='ring',
            member=self.tm8,
            tier=self.tier,
            team=self.team,
            obtained='2024-01-01',
        )
        self.b8.current_left_ring = self.raid_gear
        self.b8.save()
        # Second Floor Clear 1
        Loot.objects.create(
            item='head',
            member=self.tm3,
            tier=self.tier,
            team=self.team,
            obtained='2024-01-01',
        )
        self.b3.current_head = self.raid_gear
        self.b3.save()
        Loot.objects.create(
            item='hands',
            member=self.tm7,
            tier=self.tier,
            team=self.team,
            obtained='2024-01-01',
        )
        self.b7.current_hands = self.raid_gear
        self.b7.save()
        Loot.objects.create(
            item='feet',
            member=self.tm4,
            tier=self.tier,
            team=self.team,
            obtained='2024-01-01',
        )
        self.b4.current_feet = self.raid_gear
        self.b4.save()
        Loot.objects.create(
            item='tome-accessory-augment',
            member=self.tm6,
            tier=self.tier,
            team=self.team,
            obtained='2024-01-01',
        )
        self.b6.current_right_ring = self.tome_gear
        self.b6.save()
        # Second Floor Clear 2
        Loot.objects.create(
            item='head',
            member=self.tm2,
            tier=self.tier,
            team=self.team,
            obtained='2024-01-01',
        )
        self.b2.current_head = self.raid_gear
        self.b2.save()
        Loot.objects.create(
            item='hands',
            member=self.tm2,
            tier=self.tier,
            team=self.team,
            obtained='2024-01-01',
        )
        self.b2.current_hands = self.raid_gear
        self.b2.save()
        Loot.objects.create(
            item='feet',
            member=self.tm8,
            tier=self.tier,
            team=self.team,
            obtained='2024-01-01',
        )
        self.b8.current_feet = self.raid_gear
        self.b8.save()
        Loot.objects.create(
            item='tome-accessory-augment',
            member=self.tm7,
            tier=self.tier,
            team=self.team,
            obtained='2024-01-01',
        )
        self.b7.current_right_ring = self.tome_gear
        self.b7.save()

        url = reverse('api:loot_solver', kwargs={'team_id': self.team.pk})
        user = self._get_user()
        self.client.force_authenticate(user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        content = response.json()

        first_floor_expected = [
            {'token': False, 'Earrings': self.tm5.id, 'Necklace': self.tm1.id, 'Bracelet': self.tm6.id, 'Ring': self.tm7.id},
            {'token': True, 'Earrings': self.tm6.id, 'Necklace': self.tm2.id, 'Bracelet': self.tm4.id, 'Ring': self.tm5.id},
        ]
        first_floor_received = content['first_floor']
        self.assertEqual(len(first_floor_expected), len(first_floor_received), first_floor_received)
        for i in range(len(first_floor_expected)):
            self.assertDictEqual(first_floor_expected[i], first_floor_received[i], f'{i+1}/{len(first_floor_received)}')

        second_floor_expected = [
            {'token': False, 'Head': self.tm5.id, 'Hands': self.tm1.id, 'Feet': self.tm3.id, 'Tome Accessory Augment': self.tm8.id},
            {'token': True, 'Head': self.tm1.id, 'Hands': None, 'Feet': self.tm5.id, 'Tome Accessory Augment': self.tm2.id},
            {'token': False, 'Head': self.tm7.id, 'Hands': None, 'Feet': self.tm6.id, 'Tome Accessory Augment': self.tm1.id},
            {'token': False, 'Head': self.tm8.id, 'Hands': None, 'Feet': None, 'Tome Accessory Augment': self.tm4.id},
            {'token': True, 'Head': None, 'Hands': None, 'Feet': None, 'Tome Accessory Augment': self.tm3.id},
        ]
        second_floor_received = content['second_floor']
        self.assertEqual(len(second_floor_expected), len(second_floor_received), second_floor_received)
        for i in range(len(second_floor_expected)):
            self.assertDictEqual(second_floor_expected[i], second_floor_received[i], f'{i+1}/{len(second_floor_received)}')

        third_floor_expected = [
            {'token': False, 'Body': self.tm6.id, 'Legs': self.tm7.id, 'Tome Armour Augment': self.tm4.id},
            {'token': False, 'Body': self.tm5.id, 'Legs': self.tm1.id, 'Tome Armour Augment': self.tm8.id},
            {'token': False, 'Body': self.tm3.id, 'Legs': self.tm2.id, 'Tome Armour Augment': self.tm6.id},
            {'token': True, 'Body': self.tm4.id, 'Legs': None, 'Tome Armour Augment': self.tm7.id},
            {'token': False, 'Body': self.tm8.id, 'Legs': None, 'Tome Armour Augment': self.tm1.id},
            {'token': False, 'Body': None, 'Legs': None, 'Tome Armour Augment': self.tm5.id},
            {'token': False, 'Body': None, 'Legs': None, 'Tome Armour Augment': self.tm6.id},
            {'token': True, 'Body': None, 'Legs': None, 'Tome Armour Augment': self.tm2.id},
        ]
        third_floor_received = content['third_floor']
        self.assertEqual(len(third_floor_expected), len(third_floor_received), third_floor_received)
        for i in range(len(third_floor_expected)):
            self.assertDictEqual(third_floor_expected[i], third_floor_received[i], f'{i+1}/{len(third_floor_received)}')

        self.assertEqual(content['fourth_floor'], {'weapons': 8, 'mounts': 8})

    def test_solver_sort_overrides(self):
        """
        Ensure that overriding the solver sort order actually affects the way the members are ordered.

        expected = {
            'earrings': [self.tm5.id, self.tm6.id],
            'necklace': [self.tm1.id, self.tm2.id, self.tm3.id, self.tm4.id, self.tm7.id, self.tm8.id],
            'bracelet': [self.tm3.id, self.tm4.id, self.tm5.id, self.tm6.id],
            'ring': [self.tm5.id, self.tm6.id, self.tm7.id, self.tm8.id],
            'head': [self.tm1.id, self.tm2.id, self.tm3.id, self.tm5.id, self.tm7.id, self.tm8.id],
            'hands': [self.tm1.id, self.tm2.id, self.tm7.id],
            'feet': [self.tm3.id, self.tm4.id, self.tm5.id, self.tm6.id, self.tm8.id],
            'tome-accessory-augment': [self.tm1.id, self.tm1.id, self.tm1.id, self.tm2.id, self.tm2.id, self.tm2.id, self.tm3.id, self.tm3.id, self.tm4.id, self.tm4.id, self.tm5.id, self.tm5.id, self.tm6.id, self.tm6.id, self.tm7.id, self.tm7.id, self.tm7.id, self.tm8.id, self.tm8.id, self.tm8.id],
            'body': [self.tm3.id, self.tm4.id, self.tm5.id, self.tm6.id, self.tm8.id],
            'legs': [self.tm1.id, self.tm2.id, self.tm7.id],
            'tome-armour-augment': [self.tm1.id, self.tm1.id, self.tm2.id, self.tm2.id, self.tm3.id, self.tm3.id, self.tm4.id, self.tm4.id, self.tm4.id, self.tm5.id, self.tm5.id, self.tm6.id, self.tm6.id, self.tm6.id, self.tm7.id, self.tm7.id, self.tm8.id, self.tm8.id],
            'mainhand': [self.tm1.id, self.tm2.id, self.tm3.id, self.tm4.id, self.tm5.id, self.tm6.id, self.tm7.id, self.tm8.id],
        }
        """
        # First test while the team has no overrides to ensure the list matches what we expect
        member_order = LootSolver._get_team_solver_sort_order(self.team)
        self.assertEqual(member_order, [self.tm5.id, self.tm6.id, self.tm7.id, self.tm8.id, self.tm1.id, self.tm2.id, self.tm3.id, self.tm4.id])

        # Set some overrides and ensure the member list updates accordingly
        self.team.solver_sort_overrides = {
            'PLD': 1,
            'MNK': 19,
            'AST': 4,
            'DRK': 5,
            'BLM': 3,
            'SGE': 18,
        }
        self.team.save()
        self.team.refresh_from_db()
        member_order = LootSolver._get_team_solver_sort_order(self.team)
        self.assertEqual(member_order, [self.tm8.id, self.tm3.id, self.tm2.id, self.tm6.id, self.tm7.id, self.tm1.id, self.tm4.id, self.tm5.id])

        # Test a solver run for the team now that it has it's overridden order, ensure it works as expected
        url = reverse('api:loot_solver', kwargs={'team_id': self.team.pk})
        user = self._get_user()
        self.client.force_authenticate(user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        content = response.json()

        first_floor_expected = [
            {'token': False, 'Earrings': self.tm6.id, 'Necklace': self.tm3.id, 'Bracelet': self.tm5.id, 'Ring': self.tm8.id},
            {'token': False, 'Earrings': self.tm5.id, 'Necklace': self.tm7.id, 'Bracelet': self.tm4.id, 'Ring': self.tm6.id},
            {'token': True, 'Earrings': None, 'Necklace': self.tm2.id, 'Bracelet': self.tm3.id, 'Ring': self.tm5.id},
        ]
        first_floor_received = content['first_floor']
        self.assertEqual(len(first_floor_expected), len(first_floor_received), first_floor_received)
        for i in range(len(first_floor_expected)):
            self.assertDictEqual(first_floor_expected[i], first_floor_received[i], f'{i+1}/{len(first_floor_received)}')

        second_floor_expected = [
            {'token': False, 'Head': self.tm2.id, 'Hands': self.tm7.id, 'Feet': self.tm8.id, 'Tome Accessory Augment': self.tm1.id},
            {'token': False, 'Head': self.tm3.id, 'Hands': self.tm2.id, 'Feet': self.tm5.id, 'Tome Accessory Augment': self.tm8.id},
            {'token': True, 'Head': self.tm7.id, 'Hands': self.tm1.id, 'Feet': self.tm6.id, 'Tome Accessory Augment': self.tm4.id},
            {'token': False, 'Head': self.tm5.id, 'Hands': None, 'Feet': self.tm3.id, 'Tome Accessory Augment': self.tm2.id},
            {'token': False, 'Head': self.tm8.id, 'Hands': None, 'Feet': self.tm4.id, 'Tome Accessory Augment': self.tm7.id},
            {'token': True, 'Head': self.tm1.id, 'Hands': None, 'Feet': None, 'Tome Accessory Augment': self.tm6.id},
        ]

        second_floor_received = content['second_floor']
        self.assertEqual(len(second_floor_expected), len(second_floor_received), second_floor_received)
        for i in range(len(second_floor_expected)):
            self.assertDictEqual(second_floor_expected[i], second_floor_received[i], f'{i+1}/{len(second_floor_received)}')

        third_floor_expected = [
            {'token': False, 'Body': self.tm6.id, 'Legs': self.tm2.id, 'Tome Armour Augment': self.tm4.id},
            {'token': False, 'Body': self.tm8.id, 'Legs': self.tm7.id, 'Tome Armour Augment': self.tm3.id},
            {'token': False, 'Body': self.tm5.id, 'Legs': self.tm1.id, 'Tome Armour Augment': self.tm6.id},
            {'token': True, 'Body': self.tm4.id, 'Legs': None, 'Tome Armour Augment': self.tm2.id},
            {'token': False, 'Body': self.tm3.id, 'Legs': None, 'Tome Armour Augment': self.tm7.id},
            {'token': False, 'Body': None, 'Legs': None, 'Tome Armour Augment': self.tm8.id},
            {'token': False, 'Body': None, 'Legs': None, 'Tome Armour Augment': self.tm6.id},
            {'token': True, 'Body': None, 'Legs': None, 'Tome Armour Augment': self.tm1.id},
        ]
        third_floor_received = content['third_floor']
        self.assertEqual(len(third_floor_expected), len(third_floor_received), third_floor_received)
        for i in range(len(third_floor_expected)):
            self.assertDictEqual(third_floor_expected[i], third_floor_received[i], f'{i+1}/{len(third_floor_received)}')

    def test_handling_non_drop_gear(self):
        """
        If someone gets items outside of Fight drops, they should be removed from the list.
        Ensure that a mix and match of items obtained will return the correct info
        """
        self.b1.current_body = self.tome_gear
        self.b1.current_feet = self.tome_gear
        self.b1.save()

        Loot.objects.create(
            item='head',
            member=self.tm2,
            tier=self.tier,
            team=self.team,
            obtained='2024-01-02',
        )
        Loot.objects.create(
            item='hands',
            member=self.tm2,
            tier=self.tier,
            team=self.team,
            obtained='2024-01-02',
        )
        self.b2.current_head = self.raid_gear
        self.b2.current_hands = self.raid_gear
        self.b2.save()

        Loot.objects.create(
            item='bracelet',
            member=self.tm3,
            tier=self.tier,
            team=self.team,
            obtained='2024-01-01',
        )
        self.b3.current_bracelet = self.raid_gear
        self.b3.current_head = self.raid_gear
        self.b3.save()

        Loot.objects.create(
            item='necklace',
            member=self.tm4,
            tier=self.tier,
            team=self.team,
            obtained='2024-01-01',
        )
        self.b4.current_necklace = self.raid_gear
        self.b4.current_feet = self.raid_gear
        self.b4.save()

        Loot.objects.create(
            item='tome-accessory-augment',
            member=self.tm6,
            tier=self.tier,
            team=self.team,
            obtained='2024-01-01',
        )
        self.b6.current_right_ring = self.tome_gear
        self.b6.save()

        Loot.objects.create(
            item='hands',
            member=self.tm7,
            tier=self.tier,
            team=self.team,
            obtained='2024-01-01',
        )
        self.b7.current_hands = self.raid_gear
        self.b7.current_right_ring = self.tome_gear
        self.b7.save()

        Loot.objects.create(
            item='ring',
            member=self.tm8,
            tier=self.tier,
            team=self.team,
            obtained='2024-01-01',
        )
        self.b8.current_left_ring = self.raid_gear
        self.b8.current_feet = self.raid_gear
        self.b8.save()

        expected = {
            self.tm1.id: ['tome-armour-augment', 'tome-armour-augment'],
            self.tm2.id: [],
            self.tm3.id: ['head'],
            self.tm4.id: ['feet'],
            self.tm5.id: [],
            self.tm6.id: [],
            self.tm7.id: ['tome-accessory-augment'],
            self.tm8.id: ['feet'],
        }

        received = LootSolver._get_gear_not_obtained_from_drops(self.tier, self.team.members.all(), Loot.objects.all())
        for member_id, items in expected.items():
            self.assertEqual(items, received[member_id], member_id)

        # Also run the _get_floor_data function using the received map, ensure that the data is being used properly
        self.team.refresh_from_db()
        requirements = LootSolver._get_requirements_map(self.team)
        id_order = LootSolver._get_team_solver_sort_order(self.team)
        clears, prio_brackets, floor_data = LootSolver._get_floor_data(
            requirements,
            Loot.objects.all(),
            LootSolver.SECOND_FLOOR_SLOTS,
            id_order,
            received,
        )
        self.assertEqual(clears, 2)

        expected_prios = {
            5: [self.tm1.id],
            4: [self.tm5.id, self.tm8.id],
            3: [self.tm2.id, self.tm7.id, self.tm3.id],
            2: [self.tm6.id, self.tm4.id],
        }
        self.assertDictEqual(expected_prios, prio_brackets)

        expected_floor_data = {
            'head': [self.tm1.id, self.tm5.id, self.tm7.id, self.tm8.id],
            'hands': [self.tm1.id],
            'feet': [self.tm3.id, self.tm5.id, self.tm6.id],
            'tome-accessory-augment': [
                self.tm1.id,
                self.tm1.id,
                self.tm1.id,
                self.tm2.id,
                self.tm2.id,
                self.tm2.id,
                self.tm3.id,
                self.tm3.id,
                self.tm4.id,
                self.tm4.id,
                self.tm5.id,
                self.tm5.id,
                self.tm6.id,
                self.tm7.id,
                self.tm7.id,
                self.tm8.id,
                self.tm8.id,
                self.tm8.id,
            ],
        }
        self.assertDictEqual(expected_floor_data, floor_data)

        # Also run the second floor function and check that everything is returned in the order we expect
        second_floor_expected = [
            {'token': True, 'Head': self.tm8.id, 'Hands': self.tm1.id, 'Feet': self.tm5.id, 'Tome Accessory Augment': self.tm2.id},
            {'token': False, 'Head': self.tm1.id, 'Hands': None, 'Feet': self.tm3.id, 'Tome Accessory Augment': self.tm7.id},
            {'token': False, 'Head': self.tm5.id, 'Hands': None, 'Feet': self.tm6.id, 'Tome Accessory Augment': self.tm8.id},
            {'token': True, 'Head': self.tm7.id, 'Hands': None, 'Feet': None, 'Tome Accessory Augment': self.tm1.id},
        ]
        second_floor_received = LootSolver._get_second_floor_data(LootSolver._get_requirements_map(self.team), Loot.objects.all(), id_order, received)
        self.assertEqual(len(second_floor_expected), len(second_floor_received), second_floor_received)
        for i in range(len(second_floor_expected)):
            self.assertDictEqual(second_floor_expected[i], second_floor_received[i], f'{i+1}/{len(second_floor_received)}')


class LootSolverV2TestSuite(SavageAimTestCase):
    """
    Test cases specifically for the more clever version of the algorithm.
    Based around the current issue with M1S for us
    """

    def setUp(self):
        """
        Seed the DB
        """
        self.maxDiff = None
        call_command('seed', stdout=StringIO())

        self.tier = Tier.objects.get(max_item_level=735)
        self.team = Team.objects.create(
            invite_code=Team.generate_invite_code(),
            name='The Testers',
            tier=self.tier,
            solver_sort_overrides={'VPR': 1, 'PCT': 7},
        )
        self.raid_weapon = Gear.objects.get(item_level=735, name='Dark Horse Champion')
        self.raid_gear = Gear.objects.get(item_level=730, name='Dark Horse Champion')
        self.tome_gear = Gear.objects.get(name='Augmented Quetzalli')
        self.base_tome_gear = Gear.objects.get(name='Quetzalli')
        crafted_gear = Gear.objects.get(name='Archeo Kingdom')

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
        self.c1 = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=self._get_user(),
            name='C1',
            verified=True,
            world='Lich',
        )
        self.c2 = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=self._get_user(),
            name='C2',
            verified=True,
            world='Lich',
        )
        self.c3 = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=self._get_user(),
            name='C3',
            verified=True,
            world='Lich',
        )
        self.c4 = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=self._get_user(),
            name='C4',
            verified=True,
            world='Lich',
        )
        self.c5 = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=self._get_user(),
            name='C5',
            verified=True,
            world='Lich',
        )
        self.c6 = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=self._get_user(),
            name='C6',
            verified=True,
            world='Lich',
        )
        self.c7 = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=self._get_user(),
            name='C7',
            verified=True,
            world='Lich',
        )
        self.c8 = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=self._get_user(),
            name='C8',
            verified=True,
            world='Lich',
        )

        # Next make 8 BIS Lists, one for each, and link em to the team
        self.b1 = BISList.objects.create(
            owner=self.c1,
            job_id='DRK',
            bis_mainhand=self.raid_weapon,
            bis_offhand=self.raid_weapon,
            bis_head=self.raid_gear,
            bis_body=self.tome_gear,
            bis_hands=self.raid_gear,
            bis_legs=self.raid_gear,
            bis_feet=self.tome_gear,
            bis_earrings=self.tome_gear,
            bis_necklace=self.raid_gear,
            bis_bracelet=self.tome_gear,
            bis_right_ring=self.tome_gear,
            bis_left_ring=self.base_tome_gear,
            **current_map,
        )
        self.tm1 = self.team.members.create(character=self.c1, bis_list=self.b1, permissions=0)

        self.b2 = BISList.objects.create(
            owner=self.c2,
            job_id='GNB',
            bis_mainhand=self.raid_weapon,
            bis_offhand=self.raid_weapon,
            bis_head=self.raid_gear,
            bis_body=self.tome_gear,
            bis_hands=self.tome_gear,
            bis_legs=self.raid_gear,
            bis_feet=self.tome_gear,
            bis_earrings=self.raid_gear,
            bis_necklace=self.raid_gear,
            bis_bracelet=self.tome_gear,
            bis_right_ring=self.tome_gear,
            bis_left_ring=self.raid_gear,
            **current_map,
        )
        self.tm2 = self.team.members.create(character=self.c2, bis_list=self.b2, permissions=0)

        self.b3 = BISList.objects.create(
            owner=self.c3,
            job_id='AST',
            bis_mainhand=self.raid_weapon,
            bis_offhand=self.raid_weapon,
            bis_head=self.tome_gear,
            bis_body=self.tome_gear,
            bis_hands=crafted_gear,
            bis_legs=self.tome_gear,
            bis_feet=self.raid_gear,
            bis_earrings=self.raid_gear,
            bis_necklace=self.tome_gear,
            bis_bracelet=self.raid_gear,
            bis_right_ring=self.raid_gear,
            bis_left_ring=self.tome_gear,
            **current_map,
        )
        self.tm3 = self.team.members.create(character=self.c3, bis_list=self.b3, lead=True)

        self.b4 = BISList.objects.create(
            owner=self.c4,
            job_id='SGE',
            bis_mainhand=self.raid_weapon,
            bis_offhand=self.raid_weapon,
            bis_head=self.tome_gear,
            bis_body=self.raid_gear,
            bis_hands=crafted_gear,
            bis_legs=self.tome_gear,
            bis_feet=self.raid_gear,
            bis_earrings=self.raid_gear,
            bis_necklace=self.tome_gear,
            bis_bracelet=self.raid_gear,
            bis_right_ring=self.raid_gear,
            bis_left_ring=self.tome_gear,
            **current_map,
        )
        self.tm4 = self.team.members.create(character=self.c4, bis_list=self.b4, permissions=0)

        self.b5 = BISList.objects.create(
            owner=self.c5,
            job_id='MNK',
            bis_mainhand=self.raid_weapon,
            bis_offhand=self.raid_weapon,
            bis_head=self.tome_gear,
            bis_body=self.tome_gear,
            bis_hands=self.tome_gear,
            bis_legs=self.raid_gear,
            bis_feet=self.raid_gear,
            bis_earrings=self.tome_gear,
            bis_necklace=self.tome_gear,
            bis_bracelet=self.raid_gear,
            bis_right_ring=self.tome_gear,
            bis_left_ring=self.raid_gear,
            **current_map,
        )
        self.tm5 = self.team.members.create(character=self.c5, bis_list=self.b5, permissions=0)

        self.b6 = BISList.objects.create(
            owner=self.c6,
            job_id='VPR',
            bis_mainhand=self.raid_weapon,
            bis_offhand=self.raid_weapon,
            bis_head=self.raid_gear,
            bis_body=self.raid_gear,
            bis_hands=self.tome_gear,
            bis_legs=self.tome_gear,
            bis_feet=self.raid_gear,
            bis_earrings=self.tome_gear,
            bis_necklace=self.raid_gear,
            bis_bracelet=self.tome_gear,
            bis_right_ring=self.tome_gear,
            bis_left_ring=self.raid_gear,
            **current_map,
        )
        self.tm6 = self.team.members.create(character=self.c6, bis_list=self.b6, permissions=0)

        self.b7 = BISList.objects.create(
            owner=self.c7,
            job_id='BRD',
            bis_mainhand=self.raid_weapon,
            bis_offhand=self.raid_weapon,
            bis_head=self.raid_gear,
            bis_body=self.tome_gear,
            bis_hands=self.tome_gear,
            bis_legs=self.raid_gear,
            bis_feet=self.raid_gear,
            bis_earrings=self.tome_gear,
            bis_necklace=self.raid_gear,
            bis_bracelet=self.tome_gear,
            bis_right_ring=self.tome_gear,
            bis_left_ring=self.raid_gear,
            **current_map,
        )
        self.tm7 = self.team.members.create(character=self.c7, bis_list=self.b7, permissions=0)

        self.b8 = BISList.objects.create(
            owner=self.c8,
            job_id='PCT',
            bis_mainhand=self.raid_weapon,
            bis_offhand=self.raid_weapon,
            bis_head=self.tome_gear,
            bis_body=self.raid_gear,
            bis_hands=self.tome_gear,
            bis_legs=self.tome_gear,
            bis_feet=self.raid_gear,
            bis_earrings=self.raid_gear,
            bis_necklace=self.tome_gear,
            bis_bracelet=self.raid_gear,
            bis_right_ring=self.tome_gear,
            bis_left_ring=self.raid_gear,
            **current_map,
        )
        self.tm8 = self.team.members.create(character=self.c8, bis_list=self.b8, permissions=0)

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
        # Generate the expected map
        expected = {
            'earrings': [self.tm2.id, self.tm3.id, self.tm4.id, self.tm8.id],
            'necklace': [self.tm1.id, self.tm2.id, self.tm6.id, self.tm7.id],
            'bracelet': [self.tm3.id, self.tm4.id, self.tm5.id, self.tm8.id],
            'ring': [self.tm2.id, self.tm3.id, self.tm4.id, self.tm5.id, self.tm6.id, self.tm7.id, self.tm8.id],
            'head': [self.tm1.id, self.tm2.id, self.tm6.id, self.tm7.id],
            'hands': [self.tm1.id],
            'feet': [self.tm3.id, self.tm4.id, self.tm5.id, self.tm6.id, self.tm7.id, self.tm8.id],
            'tome-accessory-augment': [
                *([self.tm1.id] * 3),
                *([self.tm2.id] * 2),
                *([self.tm3.id] * 2),
                *([self.tm4.id] * 2),
                *([self.tm5.id] * 3),
                *([self.tm6.id] * 3),
                *([self.tm7.id] * 3),
                *([self.tm8.id] * 2),
            ],
            'body': [self.tm4.id, self.tm6.id, self.tm8.id],
            'legs': [self.tm1.id, self.tm2.id, self.tm5.id, self.tm7.id],
            'tome-armour-augment': [
                *([self.tm1.id] * 2),
                *([self.tm2.id] * 3),
                *([self.tm3.id] * 3),
                *([self.tm4.id] * 2),
                *([self.tm5.id] * 3),
                *([self.tm6.id] * 2),
                *([self.tm7.id] * 2),
                *([self.tm8.id] * 3),
            ],
            'mainhand': [self.tm1.id, self.tm2.id, self.tm3.id, self.tm4.id, self.tm5.id, self.tm6.id, self.tm7.id, self.tm8.id],
        }

        received = dict(LootSolver._get_requirements_map(self.team))
        self.assertDictEqual(expected, received)

    def test_prio_bracket_generation(self):
        """
        Create some test maps as subsets of the expected data from the last test, and get the expected priority brackets generated
        """
        first_floor_requirements = {
            'earrings': [self.tm2.id, self.tm3.id, self.tm4.id, self.tm8.id],
            'necklace': [self.tm1.id, self.tm2.id, self.tm6.id, self.tm7.id],
            'bracelet': [self.tm3.id, self.tm4.id, self.tm5.id, self.tm8.id],
            'ring': [self.tm2.id, self.tm3.id, self.tm4.id, self.tm5.id, self.tm6.id, self.tm7.id, self.tm8.id],
        }
        second_floor_requirements = {
            'head': [self.tm1.id, self.tm2.id, self.tm6.id, self.tm7.id],
            'hands': [self.tm1.id],
            'feet': [self.tm3.id, self.tm4.id, self.tm5.id, self.tm6.id, self.tm7.id, self.tm8.id],
            'tome-accessory-augment': [
                *([self.tm1.id] * 3),
                *([self.tm2.id] * 2),
                *([self.tm3.id] * 2),
                *([self.tm4.id] * 2),
                *([self.tm5.id] * 3),
                *([self.tm6.id] * 3),
                *([self.tm7.id] * 3),
                *([self.tm8.id] * 2),
            ],
        }
        third_floor_requirements = {
            'body': [self.tm4.id, self.tm6.id, self.tm8.id],
            'legs': [self.tm1.id, self.tm2.id, self.tm5.id, self.tm7.id],
            'tome-armour-augment': [
                *([self.tm1.id] * 2),
                *([self.tm2.id] * 3),
                *([self.tm3.id] * 3),
                *([self.tm4.id] * 2),
                *([self.tm5.id] * 3),
                *([self.tm6.id] * 2),
                *([self.tm7.id] * 2),
                *([self.tm8.id] * 3),
            ],
        }
        ordering = [self.tm6.id, self.tm5.id, self.tm8.id, self.tm7.id, self.tm1.id, self.tm2.id, self.tm3.id, self.tm4.id]

        first_floor_expected = {
            3: [self.tm8.id, self.tm2.id, self.tm3.id, self.tm4.id],
            2: [self.tm6.id, self.tm5.id, self.tm7.id],
            1: [self.tm1.id],
        }
        second_floor_expected = {
            5: [self.tm6.id, self.tm7.id, self.tm1.id],
            4: [self.tm5.id],
            3: [self.tm8.id, self.tm2.id, self.tm3.id, self.tm4.id],
        }
        third_floor_expected = {
            4: [self.tm5.id, self.tm8.id, self.tm2.id],
            3: [self.tm6.id, self.tm7.id, self.tm1.id, self.tm3.id, self.tm4.id],
        }

        self.assertDictEqual(LootSolver._generate_priority_brackets(first_floor_requirements, ordering), first_floor_expected)
        self.assertDictEqual(LootSolver._generate_priority_brackets(second_floor_requirements, ordering), second_floor_expected)
        self.assertDictEqual(LootSolver._generate_priority_brackets(third_floor_requirements, ordering), third_floor_expected)

    def test_whole_view(self):
        """
        Test the M1S situation against the solver algorithm, ensure that we get back the expected responses
        """

        url = reverse('api:loot_solver', kwargs={'team_id': self.team.pk})
        user = self._get_user()
        self.client.force_authenticate(user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        content = response.json()

        first_floor_expected = [
            {'token': False, 'Earrings': self.tm8.id, 'Necklace': self.tm2.id, 'Bracelet': self.tm3.id, 'Ring': self.tm4.id},
            {'token': False, 'Earrings': self.tm2.id, 'Necklace': self.tm6.id, 'Bracelet': self.tm5.id, 'Ring': self.tm7.id},
            {'token': True, 'Earrings': self.tm4.id, 'Necklace': self.tm1.id, 'Bracelet': self.tm8.id, 'Ring': self.tm3.id},
        ]
        first_floor_received = content['first_floor']
        self.assertEqual(len(first_floor_expected), len(first_floor_received), first_floor_received)
        for i in range(len(first_floor_expected)):
            self.assertDictEqual(first_floor_expected[i], first_floor_received[i], f'{i+1}/{len(first_floor_received)}')

        second_floor_expected = [
            {'token': False, 'Head': self.tm6.id, 'Hands': self.tm1.id, 'Feet': self.tm7.id, 'Tome Accessory Augment': self.tm5.id},
            {'token': False, 'Head': self.tm1.id, 'Hands': None, 'Feet': self.tm6.id, 'Tome Accessory Augment': self.tm7.id},
            {'token': True, 'Head': self.tm2.id, 'Hands': None, 'Feet': self.tm8.id, 'Tome Accessory Augment': self.tm3.id},
            {'token': False, 'Head': self.tm7.id, 'Hands': None, 'Feet': self.tm4.id, 'Tome Accessory Augment': self.tm6.id},
            {'token': False, 'Head': None, 'Hands': None, 'Feet': self.tm5.id, 'Tome Accessory Augment': self.tm1.id},
            {'token': True, 'Head': None, 'Hands': None, 'Feet': self.tm3.id, 'Tome Accessory Augment': self.tm2.id},
        ]
        second_floor_received = content['second_floor']
        self.assertEqual(len(second_floor_expected), len(second_floor_received), second_floor_received)
        for i in range(len(second_floor_expected)):
            self.assertDictEqual(second_floor_expected[i], second_floor_received[i], f'{i+1}/{len(second_floor_received)}')

        third_floor_expected = [
            {'token': False, 'Body': self.tm8.id, 'Legs': self.tm5.id, 'Tome Armour Augment': self.tm2.id},
            {'token': False, 'Body': self.tm6.id, 'Legs': self.tm7.id, 'Tome Armour Augment': self.tm1.id},
            {'token': False, 'Body': self.tm4.id, 'Legs': self.tm2.id, 'Tome Armour Augment': self.tm3.id},
            {'token': True, 'Body': None, 'Legs': self.tm1.id, 'Tome Armour Augment': self.tm8.id},
            {'token': False, 'Body': None, 'Legs': None, 'Tome Armour Augment': self.tm5.id},
            {'token': False, 'Body': None, 'Legs': None, 'Tome Armour Augment': self.tm6.id},
            {'token': False, 'Body': None, 'Legs': None, 'Tome Armour Augment': self.tm7.id},
            {'token': True, 'Body': None, 'Legs': None, 'Tome Armour Augment': self.tm3.id},
        ]
        third_floor_received = content['third_floor']
        self.assertEqual(len(third_floor_expected), len(third_floor_received), third_floor_received)
        for i in range(len(third_floor_expected)):
            self.assertDictEqual(third_floor_expected[i], third_floor_received[i], f'{i+1}/{len(third_floor_received)}')

        self.assertEqual(content['fourth_floor'], {'weapons': 8, 'mounts': 8})

    def test_whole_view_as_greedy(self):
        """
        Test the M1S situation against the solver algorithm, ensure that we get back the expected responses
        """

        url = reverse('api:loot_solver', kwargs={'team_id': self.team.pk})
        user = self._get_user()
        user.settings.loot_solver_greed = True
        user.settings.save()
        self.client.force_authenticate(user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        content = response.json()

        first_floor_expected = [
            {'token': False, 'Earrings': self.tm8.id, 'Necklace': self.tm2.id, 'Bracelet': self.tm3.id, 'Ring': self.tm4.id},
            {'token': False, 'Earrings': self.tm2.id, 'Necklace': self.tm6.id, 'Bracelet': self.tm5.id, 'Ring': self.tm7.id},
            {'token': True, 'Earrings': self.tm4.id, 'Necklace': None, 'Bracelet': self.tm8.id, 'Ring': self.tm3.id},
        ]
        first_floor_received = content['first_floor']
        self.assertEqual(len(first_floor_expected), len(first_floor_received), first_floor_received)
        for i in range(len(first_floor_expected)):
            self.assertDictEqual(first_floor_expected[i], first_floor_received[i], f'{i+1}/{len(first_floor_received)}')

        second_floor_expected = [
            {'token': False, 'Head': self.tm6.id, 'Hands': self.tm1.id, 'Feet': self.tm7.id, 'Tome Accessory Augment': self.tm5.id},
            {'token': False, 'Head': self.tm1.id, 'Hands': None, 'Feet': self.tm6.id, 'Tome Accessory Augment': self.tm7.id},
            {'token': True, 'Head': self.tm2.id, 'Hands': None, 'Feet': self.tm8.id, 'Tome Accessory Augment': self.tm3.id},
            {'token': False, 'Head': self.tm7.id, 'Hands': None, 'Feet': self.tm4.id, 'Tome Accessory Augment': self.tm6.id},
            {'token': False, 'Head': None, 'Hands': None, 'Feet': self.tm5.id, 'Tome Accessory Augment': self.tm1.id},
            {'token': True, 'Head': None, 'Hands': None, 'Feet': self.tm3.id, 'Tome Accessory Augment': None},
        ]
        second_floor_received = content['second_floor']
        self.assertEqual(len(second_floor_expected), len(second_floor_received), second_floor_received)
        for i in range(len(second_floor_expected)):
            self.assertDictEqual(second_floor_expected[i], second_floor_received[i], f'{i+1}/{len(second_floor_received)}')

        third_floor_expected = [
            {'token': False, 'Body': self.tm8.id, 'Legs': self.tm5.id, 'Tome Armour Augment': self.tm2.id},
            {'token': False, 'Body': self.tm6.id, 'Legs': self.tm7.id, 'Tome Armour Augment': self.tm1.id},
            {'token': False, 'Body': self.tm4.id, 'Legs': self.tm2.id, 'Tome Armour Augment': self.tm3.id},
            {'token': True, 'Body': None, 'Legs': self.tm1.id, 'Tome Armour Augment': self.tm8.id},
            {'token': False, 'Body': None, 'Legs': None, 'Tome Armour Augment': self.tm5.id},
            {'token': False, 'Body': None, 'Legs': None, 'Tome Armour Augment': self.tm6.id},
            {'token': False, 'Body': None, 'Legs': None, 'Tome Armour Augment': self.tm7.id},
            {'token': True, 'Body': None, 'Legs': None, 'Tome Armour Augment': None},
        ]
        third_floor_received = content['third_floor']
        self.assertEqual(len(third_floor_expected), len(third_floor_received), third_floor_received)
        for i in range(len(third_floor_expected)):
            self.assertDictEqual(third_floor_expected[i], third_floor_received[i], f'{i+1}/{len(third_floor_received)}')

        self.assertEqual(content['fourth_floor'], {'weapons': 8, 'mounts': 8})

    def test_for_single_person_requiring_loot(self):
        """
        Make it so only a single person in the team requires loot, ensure the solver manages this scenario properly
        """
        self.tm2.delete()
        self.tm3.delete()
        self.tm4.delete()
        self.tm5.delete()
        self.tm6.delete()
        self.tm7.delete()
        self.tm8.delete()
        self.team.refresh_from_db()

        # Generate the expected requirements
        expected = {
            'necklace': [self.tm1.id],

            'head': [self.tm1.id],
            'hands': [self.tm1.id],
            'tome-accessory-augment': [
                *([self.tm1.id] * 3),
            ],

            'legs': [self.tm1.id],
            'tome-armour-augment': [
                *([self.tm1.id] * 2),
            ],

            'mainhand': [self.tm1.id],
        }
        received = dict(LootSolver._get_requirements_map(self.team))
        self.assertDictEqual(expected, received)

        # Now run the solver and ensure that the single user who needs stuff is funneled items as fast as possible
        url = reverse('api:loot_solver', kwargs={'team_id': self.team.pk})
        user = self._get_user()
        self.client.force_authenticate(user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        content = response.json()

        first_floor_expected = [
            {'token': False, 'Earrings': None, 'Necklace': self.tm1.id, 'Bracelet': None, 'Ring': None},
        ]
        first_floor_received = content['first_floor']
        self.assertEqual(len(first_floor_expected), len(first_floor_received), first_floor_received)
        for i in range(len(first_floor_expected)):
            self.assertDictEqual(first_floor_expected[i], first_floor_received[i], f'{i+1}/{len(first_floor_received)}')

        second_floor_expected = [
            {'token': False, 'Head': self.tm1.id, 'Hands': self.tm1.id, 'Feet': None, 'Tome Accessory Augment': self.tm1.id},
            {'token': False, 'Head': None, 'Hands': None, 'Feet': None, 'Tome Accessory Augment': self.tm1.id},
            {'token': True, 'Head': None, 'Hands': None, 'Feet': None, 'Tome Accessory Augment': self.tm1.id},
        ]
        second_floor_received = content['second_floor']
        self.assertEqual(len(second_floor_expected), len(second_floor_received), second_floor_received)
        for i in range(len(second_floor_expected)):
            self.assertDictEqual(second_floor_expected[i], second_floor_received[i], f'{i+1}/{len(second_floor_received)}')

        third_floor_expected = [
            {'token': False, 'Body': None, 'Legs': self.tm1.id, 'Tome Armour Augment': self.tm1.id},
            {'token': False, 'Body': None, 'Legs': None, 'Tome Armour Augment': self.tm1.id},
        ]
        third_floor_received = content['third_floor']
        self.assertEqual(len(third_floor_expected), len(third_floor_received), third_floor_received)
        for i in range(len(third_floor_expected)):
            self.assertDictEqual(third_floor_expected[i], third_floor_received[i], f'{i+1}/{len(third_floor_received)}')

        # Mounts will still be 8 since it's history based
        self.assertEqual(content['fourth_floor'], {'weapons': 1, 'mounts': 1})

    def test_token_purchase_greed_assignments(self):
        """
        Test Plan:
            - Create a small test case where someone needs 2 items, and everyone else needs 1
            - Set the weeks value to be where token purchases are available
            - Ensure that the person who needs 2 items gets 1 of their required items and all other slots are greed.
        """
        prio_brackets = {
            2: [1],
            1: [2, 3, 4, 5, 6, 7, 8],
        }
        requirements = {
            'body': [],
            'legs': [1],
            'tome-armour-augment': [1, 2, 3, 4, 5, 6, 7, 8]
        }
        Loot.objects.all().delete()
        result = LootSolver._get_handout_data(
            list(requirements.keys()),
            requirements,
            prio_brackets,
            4,
            3,
        )
        self.assertEqual(len(result), 1, result)

        expected = {
            'Body': None,
            'Legs': 1,
            'Tome Armour Augment': 2,
            'token': True,
        }
        self.assertDictEqual(result[0], expected)

        # Now make the request greedy and ensure that the token is not assigned anymore
        expected['Tome Armour Augment'] = None
        prio_brackets = {
            2: [1],
            1: [2, 3, 4, 5, 6, 7, 8],
        }
        requirements = {
            'body': [],
            'legs': [1],
            'tome-armour-augment': [1, 2, 3, 4, 5, 6, 7, 8]
        }
        result = LootSolver._get_handout_data(
            list(requirements.keys()),
            requirements,
            prio_brackets,
            4,
            3,
            True,
        )
        self.assertEqual(len(result), 1, result)
        self.assertDictEqual(result[0], expected)

    def test_request_from_user_with_no_settings(self):
        """
        Test Plan:
            - Create a new user with no settings
            - Send a request and ensure that the view does not fail
        """
        url = reverse('api:loot_solver', kwargs={'team_id': self.team.pk})
        user = self._create_user()
        self.client.force_authenticate(user)
        self.c1.user = user
        self.c1.save()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)

    def test_dev_setup_edgecase_bug_solution(self):
        """
        Test Plan:
            - Set up a test case for second fight that matches the dev setup Team 1 case.
            - Ensure that the correct response is given, meaning that we get all of the loot handouts done ASAP.
        """
        requirements = {
            'head': [2, 3, 4],
            'hands': [2, 3, 4],
            'feet': [2, 4],
            'tome-accessory-augment': [2, 2, 2, 3, 3, 4, 4, 4, 4],
        }
        prio_brackets = {
            7: [4],
            6: [2],
            4: [3],
        }

        expected = [
            {'token': False, 'Head': 4, 'Hands': 3, 'Feet': 2, 'Tome Accessory Augment': 4},
            {'token': False, 'Head': 3, 'Hands': 2, 'Feet': 4, 'Tome Accessory Augment': 4},
            {'token': True, 'Head': 2, 'Hands': 4, 'Feet': None, 'Tome Accessory Augment': 3},
            {'token': False, 'Head': None, 'Hands': None, 'Feet': None, 'Tome Accessory Augment': 2},
            {'token': False, 'Head': None, 'Hands': None, 'Feet': None, 'Tome Accessory Augment': 4},
            {'token': True, 'Head': None, 'Hands': None, 'Feet': None, 'Tome Accessory Augment': 2},
        ]
        received = LootSolver._get_handout_data(
            LootSolver.SECOND_FLOOR_SLOTS,
            requirements,
            prio_brackets,
            LootSolver.SECOND_FLOOR_TOKENS,
            0,
            False,
        )
        self.assertEqual(len(expected), len(received), received)
        for i in range(len(expected)):
            self.assertDictEqual(expected[i], received[i], f'{i+1}/{len(received)}')

    def test_removed_pop_was_none_bug(self):
        """
        Test Plan:
            - Run Loot Solver with data from the latest sentry issue where it got a None.remove call
            - See what happened, and fix the bug, to make sure it never happens again
        """
        weeks = 0
        prio_brackets = {
            1: [1, 2],
            2: [3, 4, 5, 6],
        }
        floor_requirements = {
            'body': [5, 6, 3],
            'legs': [4, 1, 2],
            'tome-armour-augment': [4, 5, 6, 3],
        }

        expected = [
            {'token': False, 'Body': 3, 'Legs': 4, 'Tome Armour Augment': 5},
            {'token': False, 'Body': 6, 'Legs': 1, 'Tome Armour Augment': 4},
            {'token': False, 'Body': 5, 'Legs': 2, 'Tome Armour Augment': 3},
            {'token': True, 'Body': None, 'Legs': None, 'Tome Armour Augment': 6},
        ]

        received = LootSolver._get_handout_data(
            LootSolver.THIRD_FLOOR_SLOTS,
            floor_requirements,
            prio_brackets,
            LootSolver.THIRD_FLOOR_TOKENS,
            weeks,
            False,
        )
        self.assertEqual(len(expected), len(received), received)
        for i in range(len(expected)):
            self.assertDictEqual(expected[i], received[i], f'{i+1}/{len(received)}')

    def test_purchases_are_limited_to_tomes_only_in_midtier_fights(self):
        """
        There are some errors in the loot solver for fights 2/3 where it could be expecting armour piece buys for the same price as an augment.
        """
        weeks = 2
        second_floor_requirements = {
            'head': [1, 2, 3, 4],
            'hands': [1, 2, 5, 6],
            'feet': [5, 6, 7, 8, 3, 4],
            'tome-accessory-augment': [1, 1, 1, 2, 2, 2, 5, 5, 6, 6],
        }
        second_floor_prios = {
            5: [1, 2],
            4: [5, 6],
            2: [3, 4],
            1: [7, 8],
        }

        expected = [
            {'Head': 1, 'Hands': 2, 'Feet': 5, 'Tome Accessory Augment': 6, 'token': True},
            {'Head': 3, 'Hands': 1, 'Feet': 4, 'Tome Accessory Augment': 2, 'token': False},
            {'Head': 2, 'Hands': 5, 'Feet': 6, 'Tome Accessory Augment': 1, 'token': False},
            {'Head': 4, 'Hands': 6, 'Feet': 7, 'Tome Accessory Augment': 1, 'token': True},
            {'Head': None, 'Hands': None, 'Feet': 8, 'Tome Accessory Augment': None, 'token': False},
            {'Head': None, 'Hands': None, 'Feet': 3, 'Tome Accessory Augment': None, 'token': False},
        ]
        received = LootSolver._get_handout_data(LootSolver.SECOND_FLOOR_SLOTS, second_floor_requirements, second_floor_prios, LootSolver.SECOND_FLOOR_TOKENS, weeks, False)
        self.assertEqual(len(expected), len(received), received)
        for i in range(len(expected)):
            self.assertDictEqual(expected[i], received[i], f'{i+1}/{len(received)}')
