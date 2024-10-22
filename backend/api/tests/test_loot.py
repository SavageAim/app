from datetime import datetime, timedelta
from io import StringIO
from django.core.management import call_command
from django.urls import reverse
from rest_framework import status
from api.models import BISList, Character, Gear, Loot, Notification, Team, TeamMember, Tier
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

        # Create a Team first
        self.team = Team.objects.create(
            invite_code=Team.generate_invite_code(),
            name='Les Jambons',
            tier=Tier.objects.get(max_item_level=605),
        )

        # Create two characters belonging to separate users
        self.team_lead = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=self._get_user(),
            name='Team Lead',
            verified=True,
            world='Lich',
            alias='Leady Boi',
        )
        self.main_tank = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=self._create_user(),
            name='Main Tank',
            verified=True,
            world='Lich',
        )

        # Next, create two BIS lists for each character
        self.raid_weapon = Gear.objects.get(item_level=605, name='Asphodelos')
        self.raid_gear = Gear.objects.get(item_level=600, has_weapon=False)
        self.tome_gear = Gear.objects.get(item_level=600, has_weapon=True)
        self.crafted = Gear.objects.get(name='Classical')
        self.tl_main_bis = BISList.objects.create(
            bis_body=self.raid_gear,
            bis_bracelet=self.raid_gear,
            bis_earrings=self.raid_gear,
            bis_feet=self.raid_gear,
            bis_hands=self.tome_gear,
            bis_head=self.tome_gear,
            bis_left_ring=self.tome_gear,
            bis_legs=self.tome_gear,
            bis_mainhand=self.raid_weapon,
            bis_necklace=self.tome_gear,
            bis_offhand=self.raid_weapon,
            bis_right_ring=self.raid_gear,
            current_body=self.crafted,
            current_bracelet=self.crafted,
            current_earrings=self.crafted,
            current_feet=self.crafted,
            current_hands=self.crafted,
            current_head=self.crafted,
            current_left_ring=self.crafted,
            current_legs=self.crafted,
            current_mainhand=self.crafted,
            current_necklace=self.crafted,
            current_offhand=self.crafted,
            current_right_ring=self.crafted,
            job_id='SGE',
            owner=self.team_lead,
        )
        self.mt_alt_bis = BISList.objects.create(
            bis_body=self.raid_gear,
            bis_bracelet=self.raid_gear,
            bis_earrings=self.raid_gear,
            bis_feet=self.raid_gear,
            bis_hands=self.tome_gear,
            bis_head=self.tome_gear,
            bis_left_ring=self.tome_gear,
            bis_legs=self.tome_gear,
            bis_mainhand=self.raid_weapon,
            bis_necklace=self.tome_gear,
            bis_offhand=self.raid_weapon,
            bis_right_ring=self.raid_gear,
            current_body=self.crafted,
            current_bracelet=self.crafted,
            current_earrings=self.crafted,
            current_feet=self.crafted,
            current_hands=self.crafted,
            current_head=self.crafted,
            current_left_ring=self.crafted,
            current_legs=self.crafted,
            current_mainhand=self.crafted,
            current_necklace=self.crafted,
            current_offhand=self.crafted,
            current_right_ring=self.crafted,
            job_id='WHM',
            owner=self.main_tank,
        )
        self.tl_alt_bis = BISList.objects.create(
            bis_body=self.tome_gear,
            bis_bracelet=self.tome_gear,
            bis_earrings=self.tome_gear,
            bis_feet=self.tome_gear,
            bis_hands=self.raid_gear,
            bis_head=self.raid_gear,
            bis_left_ring=self.raid_gear,
            bis_legs=self.raid_gear,
            bis_mainhand=self.raid_weapon,
            bis_necklace=self.raid_gear,
            bis_offhand=self.raid_weapon,
            bis_right_ring=self.tome_gear,
            current_body=self.crafted,
            current_bracelet=self.crafted,
            current_earrings=self.crafted,
            current_feet=self.crafted,
            current_hands=self.crafted,
            current_head=self.crafted,
            current_left_ring=self.crafted,
            current_legs=self.crafted,
            current_mainhand=self.crafted,
            current_necklace=self.crafted,
            current_offhand=self.crafted,
            current_right_ring=self.crafted,
            job_id='PLD',
            owner=self.team_lead,
        )
        self.tl_alt_bis2 = BISList.objects.create(
            bis_body=self.tome_gear,
            bis_bracelet=self.tome_gear,
            bis_earrings=self.tome_gear,
            bis_feet=self.tome_gear,
            bis_hands=self.raid_gear,
            bis_head=self.raid_gear,
            bis_left_ring=self.raid_gear,
            bis_legs=self.raid_gear,
            bis_mainhand=self.raid_weapon,
            bis_necklace=self.raid_gear,
            bis_offhand=self.raid_weapon,
            bis_right_ring=self.tome_gear,
            current_body=self.crafted,
            current_bracelet=self.crafted,
            current_earrings=self.crafted,
            current_feet=self.crafted,
            current_hands=self.crafted,
            current_head=self.crafted,
            current_left_ring=self.crafted,
            current_legs=self.crafted,
            current_mainhand=self.crafted,
            current_necklace=self.crafted,
            current_offhand=self.crafted,
            current_right_ring=self.crafted,
            job_id='RPR',
            owner=self.team_lead,
        )
        self.mt_main_bis = BISList.objects.create(
            bis_body=self.tome_gear,
            bis_bracelet=self.tome_gear,
            bis_earrings=self.tome_gear,
            bis_feet=self.tome_gear,
            bis_hands=self.raid_gear,
            bis_head=self.raid_gear,
            bis_left_ring=self.raid_gear,
            bis_legs=self.raid_gear,
            bis_mainhand=self.raid_weapon,
            bis_necklace=self.raid_gear,
            bis_offhand=self.raid_weapon,
            bis_right_ring=self.tome_gear,
            current_body=self.crafted,
            current_bracelet=self.crafted,
            current_earrings=self.crafted,
            current_feet=self.crafted,
            current_hands=self.crafted,
            current_head=self.crafted,
            current_left_ring=self.crafted,
            current_legs=self.crafted,
            current_mainhand=self.crafted,
            current_necklace=self.crafted,
            current_offhand=self.crafted,
            current_right_ring=self.crafted,
            job_id='PLD',
            owner=self.main_tank,
        )
        self.mt_alt_bis2 = BISList.objects.create(
            bis_body=self.tome_gear,
            bis_bracelet=self.tome_gear,
            bis_earrings=self.tome_gear,
            bis_feet=self.tome_gear,
            bis_hands=self.raid_gear,
            bis_head=self.raid_gear,
            bis_left_ring=self.raid_gear,
            bis_legs=self.raid_gear,
            bis_mainhand=self.raid_weapon,
            bis_necklace=self.raid_gear,
            bis_offhand=self.raid_weapon,
            bis_right_ring=self.tome_gear,
            current_body=self.crafted,
            current_bracelet=self.crafted,
            current_earrings=self.crafted,
            current_feet=self.crafted,
            current_hands=self.crafted,
            current_head=self.crafted,
            current_left_ring=self.crafted,
            current_legs=self.crafted,
            current_mainhand=self.crafted,
            current_necklace=self.crafted,
            current_offhand=self.crafted,
            current_right_ring=self.crafted,
            job_id='DNC',
            owner=self.main_tank,
        )

        # Link the characters to the team
        self.tl_tm = self.team.members.create(character=self.team_lead, bis_list=self.tl_main_bis, lead=True)
        self.mt_tm = self.team.members.create(character=self.main_tank, bis_list=self.mt_main_bis, permissions=2)

        # Set up expected response (store it here to avoid redefining it)
        self.expected_gear = {
            'mainhand': {
                'need': [
                    {
                        'member_id': self.mt_tm.pk,
                        'character_name': f'{self.main_tank.name} @ {self.main_tank.world}',
                        'current_gear_name': self.crafted.name,
                        'current_gear_il': self.crafted.item_level,
                        'job_icon_name': 'PLD',
                        'job_role': 'tank',
                    },
                    {
                        'member_id': self.tl_tm.pk,
                        'character_name': self.team_lead.alias,
                        'current_gear_name': self.crafted.name,
                        'current_gear_il': self.crafted.item_level,
                        'job_icon_name': 'SGE',
                        'job_role': 'heal',
                    },
                ],
                'greed': [
                    {
                        'member_id': self.mt_tm.pk,
                        'character_name': f'{self.main_tank.name} @ {self.main_tank.world}',
                        'greed_lists': [
                            {
                                'bis_list_id': self.mt_alt_bis.id,
                                'bis_list_name': self.mt_alt_bis.display_name,
                                'current_gear_name': self.crafted.name,
                                'current_gear_il': self.crafted.item_level,
                                'job_icon_name': 'WHM',
                                'job_role': 'heal',
                            },
                            {
                                'bis_list_id': self.mt_alt_bis2.id,
                                'bis_list_name': self.mt_alt_bis2.display_name,
                                'current_gear_name': self.crafted.name,
                                'current_gear_il': self.crafted.item_level,
                                'job_icon_name': 'DNC',
                                'job_role': 'dps',
                            },
                        ],
                    },
                    {
                        'member_id': self.tl_tm.pk,
                        'character_name': self.team_lead.alias,
                        'greed_lists': [
                            {
                                'bis_list_id': self.tl_alt_bis.id,
                                'bis_list_name': self.tl_alt_bis.display_name,
                                'current_gear_name': self.crafted.name,
                                'current_gear_il': self.crafted.item_level,
                                'job_icon_name': 'PLD',
                                'job_role': 'tank',
                            },
                            {
                                'bis_list_id': self.tl_alt_bis2.id,
                                'bis_list_name': self.tl_alt_bis2.display_name,
                                'current_gear_name': self.crafted.name,
                                'current_gear_il': self.crafted.item_level,
                                'job_icon_name': 'RPR',
                                'job_role': 'dps',
                            },
                        ],
                    },
                ],
            },
            'head': {
                'need': [
                    {
                        'member_id': self.mt_tm.pk,
                        'character_name': f'{self.main_tank.name} @ {self.main_tank.world}',
                        'current_gear_name': self.crafted.name,
                        'current_gear_il': self.crafted.item_level,
                        'job_icon_name': 'PLD',
                        'job_role': 'tank',
                    },
                ],
                'greed': [
                    {
                        'member_id': self.mt_tm.pk,
                        'character_name': f'{self.main_tank.name} @ {self.main_tank.world}',
                        'greed_lists': [
                            {
                                'bis_list_id': self.mt_alt_bis2.id,
                                'bis_list_name': self.mt_alt_bis2.display_name,
                                'current_gear_name': self.crafted.name,
                                'current_gear_il': self.crafted.item_level,
                                'job_icon_name': 'DNC',
                                'job_role': 'dps',
                            },
                        ],
                    },
                    {
                        'member_id': self.tl_tm.pk,
                        'character_name': self.team_lead.alias,
                        'greed_lists': [
                            {
                                'bis_list_id': self.tl_alt_bis.id,
                                'bis_list_name': self.tl_alt_bis.display_name,
                                'current_gear_name': self.crafted.name,
                                'current_gear_il': self.crafted.item_level,
                                'job_icon_name': 'PLD',
                                'job_role': 'tank',
                            },
                            {
                                'bis_list_id': self.tl_alt_bis2.id,
                                'bis_list_name': self.tl_alt_bis2.display_name,
                                'current_gear_name': self.crafted.name,
                                'current_gear_il': self.crafted.item_level,
                                'job_icon_name': 'RPR',
                                'job_role': 'dps',
                            },
                        ],
                    },
                ],
            },
            'body': {
                'need': [
                    {
                        'member_id': self.tl_tm.pk,
                        'character_name': self.team_lead.alias,
                        'current_gear_name': self.crafted.name,
                        'current_gear_il': self.crafted.item_level,
                        'job_icon_name': 'SGE',
                        'job_role': 'heal',
                    },
                ],
                'greed': [
                    {
                        'member_id': self.mt_tm.pk,
                        'character_name': f'{self.main_tank.name} @ {self.main_tank.world}',
                        'greed_lists': [
                            {
                                'bis_list_id': self.mt_alt_bis.id,
                                'bis_list_name': self.mt_alt_bis.display_name,
                                'current_gear_name': self.crafted.name,
                                'current_gear_il': self.crafted.item_level,
                                'job_icon_name': 'WHM',
                                'job_role': 'heal',
                            },
                        ],
                    },
                    {
                        'member_id': self.tl_tm.pk,
                        'character_name': self.team_lead.alias,
                        'greed_lists': [],
                    },
                ],
            },
            'hands': {
                'need': [
                    {
                        'member_id': self.mt_tm.pk,
                        'character_name': f'{self.main_tank.name} @ {self.main_tank.world}',
                        'current_gear_name': self.crafted.name,
                        'current_gear_il': self.crafted.item_level,
                        'job_icon_name': 'PLD',
                        'job_role': 'tank',
                    },
                ],
                'greed': [
                    {
                        'member_id': self.mt_tm.pk,
                        'character_name': f'{self.main_tank.name} @ {self.main_tank.world}',
                        'greed_lists': [
                            {
                                'bis_list_id': self.mt_alt_bis2.id,
                                'bis_list_name': self.mt_alt_bis2.display_name,
                                'current_gear_name': self.crafted.name,
                                'current_gear_il': self.crafted.item_level,
                                'job_icon_name': 'DNC',
                                'job_role': 'dps',
                            },
                        ],
                    },
                    {
                        'member_id': self.tl_tm.pk,
                        'character_name': self.team_lead.alias,
                        'greed_lists': [
                            {
                                'bis_list_id': self.tl_alt_bis.id,
                                'bis_list_name': self.tl_alt_bis.display_name,
                                'current_gear_name': self.crafted.name,
                                'current_gear_il': self.crafted.item_level,
                                'job_icon_name': 'PLD',
                                'job_role': 'tank',
                            },
                            {
                                'bis_list_id': self.tl_alt_bis2.id,
                                'bis_list_name': self.tl_alt_bis2.display_name,
                                'current_gear_name': self.crafted.name,
                                'current_gear_il': self.crafted.item_level,
                                'job_icon_name': 'RPR',
                                'job_role': 'dps',
                            },
                        ],
                    },
                ],
            },
            'legs': {
                'need': [
                    {
                        'member_id': self.mt_tm.pk,
                        'character_name': f'{self.main_tank.name} @ {self.main_tank.world}',
                        'current_gear_name': self.crafted.name,
                        'current_gear_il': self.crafted.item_level,
                        'job_icon_name': 'PLD',
                        'job_role': 'tank',
                    },
                ],
                'greed': [
                    {
                        'member_id': self.mt_tm.pk,
                        'character_name': f'{self.main_tank.name} @ {self.main_tank.world}',
                        'greed_lists': [
                            {
                                'bis_list_id': self.mt_alt_bis2.id,
                                'bis_list_name': self.mt_alt_bis2.display_name,
                                'current_gear_name': self.crafted.name,
                                'current_gear_il': self.crafted.item_level,
                                'job_icon_name': 'DNC',
                                'job_role': 'dps',
                            },
                        ],
                    },
                    {
                        'member_id': self.tl_tm.pk,
                        'character_name': self.team_lead.alias,
                        'greed_lists': [
                            {
                                'bis_list_id': self.tl_alt_bis.id,
                                'bis_list_name': self.tl_alt_bis.display_name,
                                'current_gear_name': self.crafted.name,
                                'current_gear_il': self.crafted.item_level,
                                'job_icon_name': 'PLD',
                                'job_role': 'tank',
                            },
                            {
                                'bis_list_id': self.tl_alt_bis2.id,
                                'bis_list_name': self.tl_alt_bis2.display_name,
                                'current_gear_name': self.crafted.name,
                                'current_gear_il': self.crafted.item_level,
                                'job_icon_name': 'RPR',
                                'job_role': 'dps',
                            },
                        ],
                    },
                ],
            },
            'feet': {
                'need': [
                    {
                        'member_id': self.tl_tm.pk,
                        'character_name': self.team_lead.alias,
                        'current_gear_name': self.crafted.name,
                        'current_gear_il': self.crafted.item_level,
                        'job_icon_name': 'SGE',
                        'job_role': 'heal',
                    },
                ],
                'greed': [
                    {
                        'member_id': self.mt_tm.pk,
                        'character_name': f'{self.main_tank.name} @ {self.main_tank.world}',
                        'greed_lists': [
                            {
                                'bis_list_id': self.mt_alt_bis.id,
                                'bis_list_name': self.mt_alt_bis.display_name,
                                'current_gear_name': self.crafted.name,
                                'current_gear_il': self.crafted.item_level,
                                'job_icon_name': 'WHM',
                                'job_role': 'heal',
                            },
                        ],
                    },
                    {
                        'member_id': self.tl_tm.pk,
                        'character_name': self.team_lead.alias,
                        'greed_lists': [],
                    },
                ],
            },
            'earrings': {
                'need': [
                    {
                        'member_id': self.tl_tm.pk,
                        'character_name': self.team_lead.alias,
                        'current_gear_name': self.crafted.name,
                        'current_gear_il': self.crafted.item_level,
                        'job_icon_name': 'SGE',
                        'job_role': 'heal',
                    },
                ],
                'greed': [
                    {
                        'member_id': self.mt_tm.pk,
                        'character_name': f'{self.main_tank.name} @ {self.main_tank.world}',
                        'greed_lists': [
                            {
                                'bis_list_id': self.mt_alt_bis.id,
                                'bis_list_name': self.mt_alt_bis.display_name,
                                'current_gear_name': self.crafted.name,
                                'current_gear_il': self.crafted.item_level,
                                'job_icon_name': 'WHM',
                                'job_role': 'heal',
                            },
                        ],
                    },
                    {
                        'member_id': self.tl_tm.pk,
                        'character_name': self.team_lead.alias,
                        'greed_lists': [],
                    },
                ],
            },
            'necklace': {
                'need': [
                    {
                        'member_id': self.mt_tm.pk,
                        'character_name': f'{self.main_tank.name} @ {self.main_tank.world}',
                        'current_gear_name': self.crafted.name,
                        'current_gear_il': self.crafted.item_level,
                        'job_icon_name': 'PLD',
                        'job_role': 'tank',
                    },
                ],
                'greed': [
                    {
                        'member_id': self.mt_tm.pk,
                        'character_name': f'{self.main_tank.name} @ {self.main_tank.world}',
                        'greed_lists': [
                            {
                                'bis_list_id': self.mt_alt_bis2.id,
                                'bis_list_name': self.mt_alt_bis2.display_name,
                                'current_gear_name': self.crafted.name,
                                'current_gear_il': self.crafted.item_level,
                                'job_icon_name': 'DNC',
                                'job_role': 'dps',
                            },
                        ],
                    },
                    {
                        'member_id': self.tl_tm.pk,
                        'character_name': self.team_lead.alias,
                        'greed_lists': [
                            {
                                'bis_list_id': self.tl_alt_bis.id,
                                'bis_list_name': self.tl_alt_bis.display_name,
                                'current_gear_name': self.crafted.name,
                                'current_gear_il': self.crafted.item_level,
                                'job_icon_name': 'PLD',
                                'job_role': 'tank',
                            },
                            {
                                'bis_list_id': self.tl_alt_bis2.id,
                                'bis_list_name': self.tl_alt_bis2.display_name,
                                'current_gear_name': self.crafted.name,
                                'current_gear_il': self.crafted.item_level,
                                'job_icon_name': 'RPR',
                                'job_role': 'dps',
                            },
                        ],
                    },
                ],
            },
            'bracelet': {
                'need': [
                    {
                        'member_id': self.tl_tm.pk,
                        'character_name': self.team_lead.alias,
                        'current_gear_name': self.crafted.name,
                        'current_gear_il': self.crafted.item_level,
                        'job_icon_name': 'SGE',
                        'job_role': 'heal',
                    },
                ],
                'greed': [
                    {
                        'member_id': self.mt_tm.pk,
                        'character_name': f'{self.main_tank.name} @ {self.main_tank.world}',
                        'greed_lists': [
                            {
                                'bis_list_id': self.mt_alt_bis.id,
                                'bis_list_name': self.mt_alt_bis.display_name,
                                'current_gear_name': self.crafted.name,
                                'current_gear_il': self.crafted.item_level,
                                'job_icon_name': 'WHM',
                                'job_role': 'heal',
                            },
                        ],
                    },
                    {
                        'member_id': self.tl_tm.pk,
                        'character_name': self.team_lead.alias,
                        'greed_lists': [],
                    },
                ],
            },
            'ring': {
                'need': [
                    {
                        'member_id': self.mt_tm.pk,
                        'character_name': f'{self.main_tank.name} @ {self.main_tank.world}',
                        'current_gear_name': self.crafted.name,
                        'current_gear_il': self.crafted.item_level,
                        'job_icon_name': 'PLD',
                        'job_role': 'tank',
                    },
                    {
                        'member_id': self.tl_tm.pk,
                        'character_name': self.team_lead.alias,
                        'current_gear_name': self.crafted.name,
                        'current_gear_il': self.crafted.item_level,
                        'job_icon_name': 'SGE',
                        'job_role': 'heal',
                    },
                ],
                'greed': [
                    {
                        'member_id': self.mt_tm.pk,
                        'character_name': f'{self.main_tank.name} @ {self.main_tank.world}',
                        'greed_lists': [
                            {
                                'bis_list_id': self.mt_alt_bis.id,
                                'bis_list_name': self.mt_alt_bis.display_name,
                                'current_gear_name': self.crafted.name,
                                'current_gear_il': self.crafted.item_level,
                                'job_icon_name': 'WHM',
                                'job_role': 'heal',
                            },
                            {
                                'bis_list_id': self.mt_alt_bis2.id,
                                'bis_list_name': self.mt_alt_bis2.display_name,
                                'current_gear_name': self.crafted.name,
                                'current_gear_il': self.crafted.item_level,
                                'job_icon_name': 'DNC',
                                'job_role': 'dps',
                            },
                        ],
                    },
                    {
                        'member_id': self.tl_tm.pk,
                        'character_name': self.team_lead.alias,
                        'greed_lists': [
                            {
                                'bis_list_id': self.tl_alt_bis.id,
                                'bis_list_name': self.tl_alt_bis.display_name,
                                'current_gear_name': self.crafted.name,
                                'current_gear_il': self.crafted.item_level,
                                'job_icon_name': 'PLD',
                                'job_role': 'tank',
                            },
                            {
                                'bis_list_id': self.tl_alt_bis2.id,
                                'bis_list_name': self.tl_alt_bis2.display_name,
                                'current_gear_name': self.crafted.name,
                                'current_gear_il': self.crafted.item_level,
                                'job_icon_name': 'RPR',
                                'job_role': 'dps',
                            },
                        ],
                    },
                ],
            },
            'tome-accessory-augment': {
                'need': [
                    {
                        'member_id': self.mt_tm.pk,
                        'character_name': f'{self.main_tank.name} @ {self.main_tank.world}',
                        'job_icon_name': 'PLD',
                        'job_role': 'tank',
                        'requires': 3,
                    },
                    {
                        'member_id': self.tl_tm.pk,
                        'character_name': self.team_lead.alias,
                        'job_icon_name': 'SGE',
                        'job_role': 'heal',
                        'requires': 2,
                    },
                ],
                'greed': [
                    {
                        'member_id': self.mt_tm.pk,
                        'character_name': f'{self.main_tank.name} @ {self.main_tank.world}',
                        'greed_lists': [
                            {
                                'bis_list_id': self.mt_alt_bis.id,
                                'bis_list_name': self.mt_alt_bis.display_name,
                                'job_icon_name': 'WHM',
                                'job_role': 'heal',
                                'requires': 2,
                            },
                            {
                                'bis_list_id': self.mt_alt_bis2.id,
                                'bis_list_name': self.mt_alt_bis2.display_name,
                                'job_icon_name': 'DNC',
                                'job_role': 'dps',
                                'requires': 3,
                            },
                        ],
                    },
                    {
                        'member_id': self.tl_tm.pk,
                        'character_name': self.team_lead.alias,
                        'greed_lists': [
                            {
                                'bis_list_id': self.tl_alt_bis.id,
                                'bis_list_name': self.tl_alt_bis.display_name,
                                'job_icon_name': 'PLD',
                                'job_role': 'tank',
                                'requires': 3,
                            },
                            {
                                'bis_list_id': self.tl_alt_bis2.id,
                                'bis_list_name': self.tl_alt_bis2.display_name,
                                'job_icon_name': 'RPR',
                                'job_role': 'dps',
                                'requires': 3,
                            },
                        ],
                    },
                ],
            },
            'tome-armour-augment': {
                'need': [
                    {
                        'member_id': self.mt_tm.pk,
                        'character_name': f'{self.main_tank.name} @ {self.main_tank.world}',
                        'job_icon_name': 'PLD',
                        'job_role': 'tank',
                        'requires': 2,
                    },
                    {
                        'member_id': self.tl_tm.pk,
                        'character_name': self.team_lead.alias,
                        'job_icon_name': 'SGE',
                        'job_role': 'heal',
                        'requires': 3,
                    },
                ],
                'greed': [
                    {
                        'member_id': self.mt_tm.pk,
                        'character_name': f'{self.main_tank.name} @ {self.main_tank.world}',
                        'greed_lists': [
                            {
                                'bis_list_id': self.mt_alt_bis.id,
                                'bis_list_name': self.mt_alt_bis.display_name,
                                'job_icon_name': 'WHM',
                                'job_role': 'heal',
                                'requires': 3,
                            },
                            {
                                'bis_list_id': self.mt_alt_bis2.id,
                                'bis_list_name': self.mt_alt_bis2.display_name,
                                'job_icon_name': 'DNC',
                                'job_role': 'dps',
                                'requires': 2,
                            },
                        ],
                    },
                    {
                        'member_id': self.tl_tm.pk,
                        'character_name': self.team_lead.alias,
                        'greed_lists': [
                            {
                                'bis_list_id': self.tl_alt_bis.id,
                                'bis_list_name': self.tl_alt_bis.display_name,
                                'job_icon_name': 'PLD',
                                'job_role': 'tank',
                                'requires': 2,
                            },
                            {
                                'bis_list_id': self.tl_alt_bis2.id,
                                'bis_list_name': self.tl_alt_bis2.display_name,
                                'job_icon_name': 'RPR',
                                'job_role': 'dps',
                                'requires': 2,
                            },
                        ],
                    },
                ],
            },
            'mount': {
                'need': [
                    {
                        'member_id': self.mt_tm.pk,
                        'character_name': f'{self.main_tank.name} @ {self.main_tank.world}',
                        'current_gear_name': 'N/A',
                        'current_gear_il': 'N/A',
                        'job_icon_name': 'PLD',
                        'job_role': 'tank',
                    },
                    {
                        'member_id': self.tl_tm.pk,
                        'character_name': self.team_lead.alias,
                        'current_gear_name': 'N/A',
                        'current_gear_il': 'N/A',
                        'job_icon_name': 'SGE',
                        'job_role': 'heal',
                    },
                ],
                'greed': [],
            },
            'tome-weapon-token': {
                'need': [
                    {
                        'member_id': self.mt_tm.pk,
                        'character_name': f'{self.main_tank.name} @ {self.main_tank.world}',
                        'current_gear_name': self.mt_main_bis.current_mainhand.name,
                        'current_gear_il': self.mt_main_bis.current_mainhand.item_level,
                        'job_icon_name': 'PLD',
                        'job_role': 'tank',
                    },
                    {
                        'member_id': self.tl_tm.pk,
                        'character_name': self.team_lead.alias,
                        'current_gear_name': self.tl_main_bis.current_mainhand.name,
                        'current_gear_il': self.tl_main_bis.current_mainhand.item_level,
                        'job_icon_name': 'SGE',
                        'job_role': 'heal',
                    },
                ],
                'greed': [
                    {
                        'member_id': self.mt_tm.pk,
                        'character_name': f'{self.main_tank.name} @ {self.main_tank.world}',
                        'greed_lists': [],
                    },
                    {
                        'member_id': self.tl_tm.pk,
                        'character_name': self.team_lead.alias,
                        'greed_lists': [],
                    },
                ],
            },
            'tome-weapon-augment': {
                'need': [
                    {
                        'member_id': self.mt_tm.pk,
                        'character_name': f'{self.main_tank.name} @ {self.main_tank.world}',
                        'current_gear_name': self.mt_main_bis.current_mainhand.name,
                        'current_gear_il': self.mt_main_bis.current_mainhand.item_level,
                        'job_icon_name': 'PLD',
                        'job_role': 'tank',
                    },
                    {
                        'member_id': self.tl_tm.pk,
                        'character_name': self.team_lead.alias,
                        'current_gear_name': self.tl_main_bis.current_mainhand.name,
                        'current_gear_il': self.tl_main_bis.current_mainhand.item_level,
                        'job_icon_name': 'SGE',
                        'job_role': 'heal',
                    },
                ],
                'greed': [
                    {
                        'member_id': self.mt_tm.pk,
                        'character_name': f'{self.main_tank.name} @ {self.main_tank.world}',
                        'greed_lists': [],
                    },
                    {
                        'member_id': self.tl_tm.pk,
                        'character_name': self.team_lead.alias,
                        'greed_lists': [],
                    },
                ],
            },
        }

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

    def test_calculator(self):
        """
        Given the objects we set up, test that the calculator returns the correct information
        Then update some BIS items and recheck to ensure it's always up to date
        """
        # Add some history elements for testing the new stuff
        Loot.objects.create(
            greed=False,
            item='mount',
            member=self.mt_tm,
            obtained=datetime.now(),
            team=self.team,
            tier=self.team.tier,
        )
        Loot.objects.create(
            greed=False,
            item='tome-weapon-token',
            member=self.tl_tm,
            obtained=datetime.now(),
            team=self.team,
            tier=self.team.tier,
        )
        self.expected_gear['mount']['need'].pop(0)
        self.expected_gear['tome-weapon-token']['need'].pop(1)

        url = reverse('api:loot_collection', kwargs={'team_id': self.team.pk})
        user = self._get_user()
        self.client.force_authenticate(user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Compile the expected gear response and ensure it all matches
        content = response.json()['loot']['gear']
        self.assertEqual(len(content), len(self.expected_gear), content)
        for item in self.expected_gear.keys():
            self.assertEqual(content[item], self.expected_gear[item], item)

        # Update some of the BIS Lists, remove the equivalent from the local response and check again
        self.tl_main_bis.current_mainhand = self.raid_weapon
        self.tl_main_bis.current_feet = self.raid_gear
        self.tl_main_bis.current_right_ring = self.raid_gear
        self.tl_main_bis.save()

        self.expected_gear['tome-weapon-augment']['need'][1].update(
            {'current_gear_il': self.raid_weapon.item_level, 'current_gear_name': self.raid_weapon.name},
        )
        self.expected_gear['mainhand']['need'].pop(1)
        self.expected_gear['feet']['need'].pop(0)
        self.expected_gear['ring']['need'].pop(1)

        self.tl_alt_bis.current_mainhand = self.raid_weapon
        self.tl_alt_bis.current_legs = self.raid_gear
        self.tl_alt_bis.current_left_ring = self.raid_gear
        self.tl_alt_bis.save()

        self.expected_gear['mainhand']['greed'][1]['greed_lists'].pop(0)
        self.expected_gear['legs']['greed'][1]['greed_lists'].pop(0)
        self.expected_gear['ring']['greed'][1]['greed_lists'].pop(0)

        self.tl_alt_bis2.current_mainhand = self.raid_weapon
        self.tl_alt_bis2.current_head = self.raid_gear
        self.tl_alt_bis2.current_necklace = self.raid_gear
        self.tl_alt_bis2.save()

        self.expected_gear['mainhand']['greed'][1]['greed_lists'].pop(0)
        self.expected_gear['head']['greed'][1]['greed_lists'].pop(1)
        self.expected_gear['necklace']['greed'][1]['greed_lists'].pop(1)

        self.mt_main_bis.current_mainhand = self.raid_weapon
        self.mt_main_bis.current_hands = self.raid_gear
        self.mt_main_bis.save()

        self.expected_gear['tome-weapon-token']['need'][0].update(
            {'current_gear_il': self.raid_weapon.item_level, 'current_gear_name': self.raid_weapon.name},
        )
        self.expected_gear['tome-weapon-augment']['need'][0].update(
            {'current_gear_il': self.raid_weapon.item_level, 'current_gear_name': self.raid_weapon.name},
        )
        self.expected_gear['mainhand']['need'].pop(0)
        self.expected_gear['hands']['need'].pop(0)

        self.mt_alt_bis.current_mainhand = self.raid_weapon
        self.mt_alt_bis.current_body = self.raid_gear
        self.mt_alt_bis.current_right_ring = self.raid_gear
        self.mt_alt_bis.save()

        self.expected_gear['mainhand']['greed'][0]['greed_lists'].pop(0)
        self.expected_gear['body']['greed'][0]['greed_lists'].pop(0)
        self.expected_gear['ring']['greed'][0]['greed_lists'].pop(0)

        self.mt_alt_bis2.current_legs = self.raid_gear
        self.mt_alt_bis2.current_head = self.raid_gear
        self.mt_alt_bis2.current_necklace = self.raid_gear
        self.mt_alt_bis2.save()

        self.expected_gear['legs']['greed'][0]['greed_lists'].pop(0)
        self.expected_gear['head']['greed'][0]['greed_lists'].pop(0)
        self.expected_gear['necklace']['greed'][0]['greed_lists'].pop(0)

        # Upgrade some tome gear and check required numbers
        aug_tome_gear = Gear.objects.get(name='Augmented Radiant Host')
        self.mt_main_bis.current_body = aug_tome_gear
        self.mt_main_bis.save()
        self.tl_alt_bis2.current_right_ring = aug_tome_gear
        self.tl_alt_bis2.save()

        self.expected_gear['tome-armour-augment']['need'][0]['requires'] -= 1
        self.expected_gear['tome-accessory-augment']['greed'][1]['greed_lists'][1]['requires'] -= 1

        # Send request and retest with updated expectation
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        content = response.json()['loot']['gear']
        self.assertEqual(len(content), len(self.expected_gear), content)
        for item in self.expected_gear.keys():
            self.assertEqual(content[item], self.expected_gear[item], item)

    def test_history(self):
        """
        Do a test of the history part of the list and ensure that the response is correct
        """
        url = reverse('api:loot_collection', kwargs={'team_id': self.team.pk})
        user = self._get_user()
        self.client.force_authenticate(user)

        # Create some loot items and then send a request and ensure the appropriate history is returned
        l3 = Loot.objects.create(
            greed=False,
            item='mount',
            member=self.tl_tm,
            team=self.team,
            obtained=datetime.today(),
            tier=self.team.tier,
        )  # 3
        l2 = Loot.objects.create(
            greed=False,
            item='body',
            member=self.mt_tm,
            team=self.team,
            obtained=datetime.today(),
            tier=self.team.tier,
        )  # 2
        l1 = Loot.objects.create(
            greed=True,
            item='mainhand',
            member=self.tl_tm,
            team=self.team,
            obtained=datetime.today(),
            tier=self.team.tier,
        )  # 1
        l4 = Loot.objects.create(
            greed=False,
            item='tome-armour-augment',
            member=self.mt_tm,
            team=self.team,
            obtained=datetime.today() - timedelta(days=2),
            tier=self.team.tier,
        )  # 4
        l5 = Loot.objects.create(
            greed=False,
            item='tome-armour-augment',
            member=None,
            team=self.team,
            obtained=datetime.today() - timedelta(days=7),
            tier=self.team.tier,
        )  # 5

        history = [
            {
                'greed': True,
                'item': 'Mainhand',
                'member': self.team_lead.alias,
                'obtained': l1.obtained.strftime('%Y-%m-%d'),
                'id': l1.pk,
            },
            {
                'greed': False,
                'item': 'Body',
                'member': f'{self.main_tank.name} @ {self.main_tank.world}',
                'obtained': l1.obtained.strftime('%Y-%m-%d'),
                'id': l2.pk,
            },
            {
                'greed': False,
                'item': 'Mount',
                'member': self.team_lead.alias,
                'obtained': l1.obtained.strftime('%Y-%m-%d'),
                'id': l3.pk,
            },
            {
                'greed': False,
                'item': 'Tome Armour Augment',
                'member': f'{self.main_tank.name} @ {self.main_tank.world}',
                'obtained': l4.obtained.strftime('%Y-%m-%d'),
                'id': l4.pk,
            },
            {
                'greed': False,
                'item': 'Tome Armour Augment',
                'member': 'Old Member',
                'obtained': l5.obtained.strftime('%Y-%m-%d'),
                'id': l5.pk,
            },
        ]

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        content = response.json()['loot']['history']
        self.assertEqual(len(content), 5)
        for i in range(len(content)):
            self.assertDictEqual(content[i], history[i])

    def test_create(self):
        """
        Create just a loot record for an item not tracked using the need/greed gear system
        """
        url = reverse('api:loot_collection', kwargs={'team_id': self.team.pk})
        user = self._get_user()
        self.client.force_authenticate(user)
        obtained = datetime.today().strftime('%Y-%m-%d')

        data = {
            'greed': False,
            'member_id': self.tl_tm.pk,
            'item': 'mount',
            'obtained': obtained,
        }
        # Also test creating one for tomorrow which should be allowed due to timezone issues
        obtained = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')
        greed_data = {
            'greed': True,
            'member_id': self.mt_tm.pk,
            'item': 'tome-armour-augment',
            'obtained': obtained,
        }
        need_response = self.client.post(url, data)
        self.assertEqual(need_response.status_code, status.HTTP_201_CREATED, need_response.content)

        # Test with non leader with permissions
        self.tl_tm.lead = False
        self.tl_tm.permissions = TeamMember.PERMISSION_FLAGS['loot_manager']
        self.tl_tm.save()
        greed_response = self.client.post(url, greed_data)
        self.assertEqual(greed_response.status_code, status.HTTP_201_CREATED, greed_response.content)

        self.assertEqual(Loot.objects.count(), 2)
        greed = Loot.objects.first()
        need = Loot.objects.last()

        self.assertTrue(greed.greed)
        self.assertEqual(greed.member, self.mt_tm)
        self.assertEqual(greed.item, 'tome-armour-augment')
        self.assertFalse(need.greed)
        self.assertEqual(need.member, self.tl_tm)
        self.assertEqual(need.item, 'mount')

    def test_create_400(self):
        """
        Test invalid creation cases for base loot api and ensure appropriate errors are returned

        Member ID not sent: 'This field is required.'
        Member ID not int: 'A valid integer is required.'
        Member ID not valid Member: 'Please select a Character that is a member of the Team.'
        Item not sent: 'This field is required.'
        Item not in valid list: 'Please select a valid item.'
        Greed not bool: 'Must be a valid boolean.'
        Obtained not sent: 'This field is required.'
        Obtained not valid date: 'Date has wrong format. Use one of these formats instead: YYYY-MM-DD.'
        Obtained in the future: 'Cannot record Loot for a date in the future.'
        """
        url = reverse('api:loot_collection', kwargs={'team_id': self.team.pk})
        user = self._get_user()
        self.client.force_authenticate(user)

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        content = response.json()
        self.assertEqual(content['member_id'], ['This field is required.'])
        self.assertEqual(content['item'], ['This field is required.'])
        self.assertEqual(content['obtained'], ['This field is required.'])

        data = {
            'member_id': 'abcde',
            'item': 'new-car',
            'greed': 'abcde',
            'obtained': 'abcde',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        content = response.json()
        self.assertEqual(content['member_id'], ['A valid integer is required.'])
        self.assertEqual(content['item'], ['Please select a valid item.'])
        self.assertEqual(content['greed'], ['Must be a valid boolean.'])
        self.assertEqual(content['obtained'], ['Date has wrong format. Use one of these formats instead: YYYY-MM-DD.'])

        data = {
            'member_id': '9999999',
            'obtained': (datetime.today() + timedelta(days=2)).strftime('%Y-%m-%d'),
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        content = response.json()
        self.assertEqual(content['member_id'], ['Please select a Character that is a member of the Team.'])
        self.assertEqual(content['obtained'], ['Cannot record Loot for a date in the future.'])

    def test_create_with_bis(self):
        """
        Create BIS Loot records, test the need/greed calculator to see the updates have been saved
        """
        read_url = reverse('api:loot_collection', kwargs={'team_id': self.team.pk})
        write_url = reverse('api:loot_with_bis', kwargs={'team_id': self.team.pk})
        user = self._get_user()
        self.client.force_authenticate(user)

        # We don't have to check initial values only post values
        need_data_ring = {
            'greed': False,
            'member_id': self.tl_tm.pk,
            'item': 'ring',
            'greed_bis_id': None,
        }
        need_data_shield = {
            'greed': False,
            'member_id': self.mt_tm.pk,
            'item': 'mainhand',
        }
        need_data_body = {
            'greed': False,
            'member_id': self.tl_tm.pk,
            'item': 'body',
        }
        need_data_mainhand = {
            'greed': False,
            'member_id': self.tl_tm.pk,
            'item': 'mainhand'
        }
        greed_data_ring = {
            'greed': True,
            'member_id': self.mt_tm.pk,
            'item': 'ring',
            'greed_bis_id': self.mt_alt_bis2.pk,
        }
        greed_data_shield = {
            'greed': True,
            'member_id': self.tl_tm.pk,
            'item': 'mainhand',
            'greed_bis_id': self.tl_alt_bis.pk,
        }
        greed_data_body = {
            'greed': True,
            'member_id': self.mt_tm.pk,
            'item': 'body',
            'greed_bis_id': self.mt_alt_bis.pk,
        }

        # Update expected data
        self.expected_gear['ring']['need'].pop(1)
        self.expected_gear['mainhand']['need'].pop(0)
        self.expected_gear['mainhand']['need'].pop(0)
        self.expected_gear['body']['need'].pop(0)
        self.expected_gear['ring']['greed'][0]['greed_lists'].pop(1)
        self.expected_gear['mainhand']['greed'][1]['greed_lists'].pop(0)
        self.expected_gear['body']['greed'][0]['greed_lists'].pop(0)
        self.expected_gear['tome-weapon-token']['need'][0].update(
            {'current_gear_il': self.raid_weapon.item_level, 'current_gear_name': self.raid_weapon.name},
        )
        self.expected_gear['tome-weapon-augment']['need'][0].update(
            {'current_gear_il': self.raid_weapon.item_level, 'current_gear_name': self.raid_weapon.name},
        )
        self.expected_gear['tome-weapon-token']['need'][1].update(
            {'current_gear_il': self.raid_weapon.item_level, 'current_gear_name': self.raid_weapon.name},
        )
        self.expected_gear['tome-weapon-augment']['need'][1].update(
            {'current_gear_il': self.raid_weapon.item_level, 'current_gear_name': self.raid_weapon.name},
        )

        self.assertEqual(self.client.post(write_url, need_data_ring).status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.client.post(write_url, need_data_shield).status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.client.post(write_url, need_data_body).status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.client.post(write_url, need_data_mainhand).status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.client.post(write_url, greed_data_ring).status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.client.post(write_url, greed_data_shield).status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.client.post(write_url, greed_data_body).status_code, status.HTTP_201_CREATED)

        self.assertEqual(Loot.objects.count(), 7)

        # Send a request to the read url and check the response vs the expected gear
        response = self.client.get(read_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        content = response.json()['loot']['gear']
        for item in self.expected_gear.keys():
            self.assertEqual(content[item], self.expected_gear[item], item)

        # Check the objects themselves
        self.tl_main_bis.refresh_from_db()
        self.assertEqual(self.tl_main_bis.bis_right_ring_id, self.raid_gear.pk)
        self.assertEqual(self.tl_main_bis.bis_body_id, self.raid_gear.pk)
        self.assertEqual(self.tl_main_bis.bis_mainhand_id, self.raid_weapon.pk)
        self.assertEqual(self.tl_main_bis.bis_offhand_id, self.raid_weapon.pk)
        self.mt_main_bis.refresh_from_db()
        self.assertEqual(self.mt_main_bis.bis_offhand_id, self.raid_weapon.pk)
        self.mt_alt_bis2.refresh_from_db()
        self.assertEqual(self.mt_alt_bis2.bis_left_ring_id, self.raid_gear.pk)
        self.tl_alt_bis.refresh_from_db()
        self.assertEqual(self.tl_alt_bis.bis_offhand_id, self.raid_weapon.pk)
        self.mt_alt_bis.refresh_from_db()
        self.assertEqual(self.mt_alt_bis.bis_body_id, self.raid_gear.pk)

    def test_create_with_bis_notification(self):
        """
        Do the same as above, but only once, and check the Notification status
        """
        write_url = reverse('api:loot_with_bis', kwargs={'team_id': self.team.pk})
        user = self._get_user()
        self.client.force_authenticate(user)

        # We don't have to check initial values only post values
        data = {
            'greed': False,
            'member_id': self.tl_tm.pk,
            'item': 'ring',
            'greed_bis_id': None,
        }

        self.assertEqual(self.client.post(write_url, data).status_code, status.HTTP_201_CREATED)

        # The only thing we need to check is the status of Notifications
        self.assertEqual(Notification.objects.filter(user=self.team_lead.user).count(), 1)
        notif = Notification.objects.filter(user=self.team_lead.user).first()
        self.assertEqual(notif.link, f'/characters/{self.team_lead.id}/bis_list/{self.tl_main_bis.id}/')
        self.assertEqual(
            notif.text,
            f'"{self.team_lead}"\'s BIS List "{self.tl_main_bis}" was updated via "{self.team.name}"\'s Loot Tracker!',
        )
        self.assertEqual(notif.type, 'loot_tracker_update')
        self.assertFalse(notif.read)

    def test_create_with_bis_400(self):
        """
        Test invalid creation cases for with bis loot api and ensure appropriate errors are returned

        Greed not sent: 'This field is required.'
        Greed not valid boolean: 'Must be a valid boolean.'
        Greed BIS ID not int: 'A valid integer is required.'
        Greed BIS ID doesn't belong to someone on the team: 'Please select a valid BIS List owned by a team member.'
        Greed BIS ID not sent for greed=True request: 'This field is required for Greed loot entries.'
        Greed BIS ID belongs to another member: 'Please select a valid BIS List owned by a team member.'
        Greed BIS ID is the id of the main bis for the team member:
            'To add Loot to the BIS List this Member has associated with the team, please set greed=false.'
        Item not sent: 'This field is required.'
        Invalid item: 'Please select a valid item.'
        Offhand item for non PLD BIS: 'Offhand items can only be obtained by a PLD.'
        No rings use raid as bis: 'The chosen item in the specified BIS List does not have raid loot as its BIS.'
        Item BIS isn't raid: 'The chosen item in the specified BIS List does not have raid loot as its BIS.'
        Member ID not sent: 'This field is required.'
        Member ID not int: 'A valid integer is required.'
        Member ID not valid Member: 'Please select a Character that is a member of the Team.'
        """
        url = reverse('api:loot_with_bis', kwargs={'team_id': self.team.pk})
        user = self._get_user()
        self.client.force_authenticate(user)

        data = {}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        content = response.json()
        self.assertEqual(content['member_id'], ['This field is required.'])
        self.assertEqual(content['item'], ['This field is required.'])
        self.assertEqual(content['greed'], ['This field is required.'])

        data = {
            'greed': 'abcde',
            'greed_bis_id': 'abcde',
            'item': 'abcde',
            'member_id': 'abcde',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        content = response.json()
        self.assertEqual(content['member_id'], ['A valid integer is required.'])
        self.assertEqual(content['item'], ['Please select a valid item.'])
        self.assertEqual(content['greed'], ['Must be a valid boolean.'])
        self.assertEqual(content['greed_bis_id'], ['A valid integer is required.'])

        data = {
            'greed': False,
            'greed_bis_id': '99999',
            'item': 'mainhand',
            'member_id': '99999',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        content = response.json()
        self.assertEqual(content['member_id'], ['Please select a Character that is a member of the Team.'])
        self.assertEqual(content['greed_bis_id'], ['Please select a valid BIS List owned by a team member.'])

        data = {
            'greed': True,
            'greed_bis_id': None,
            'item': 'mainhand',
            'member_id': self.tl_tm.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        content = response.json()
        self.assertEqual(content['greed_bis_id'], ['This field is required for Greed loot entries.'])

        data = {
            'greed': True,
            'greed_bis_id': self.mt_alt_bis.pk,
            'item': 'mainhand',
            'member_id': self.tl_tm.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        content = response.json()
        self.assertEqual(content['greed_bis_id'], ['Please select a valid BIS List owned by a team member.'])

        data = {
            'greed': True,
            'greed_bis_id': self.tl_main_bis.pk,
            'item': 'mainhand',
            'member_id': self.tl_tm.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        content = response.json()
        self.assertEqual(
            content['greed_bis_id'],
            ['To add Loot to the BIS List this Member has associated with the team, please set greed=false.'],
        )

        # data = {
        #     'greed': True,
        #     'greed_bis_id': self.tl_alt_bis2.pk,
        #     'item': 'mainhand',
        #     'member_id': self.tl_tm.pk,
        # }
        # response = self.client.post(url, data)
        # self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # content = response.json()
        # self.assertEqual(content['item'], ['Offhand items can only be obtained by a PLD.'])

        self.tl_alt_bis2.bis_body = self.tome_gear
        self.tl_alt_bis2.bis_left_ring = self.tome_gear
        self.tl_alt_bis2.save()

        data = {
            'greed': True,
            'greed_bis_id': self.tl_alt_bis2.pk,
            'item': 'ring',
            'member_id': self.tl_tm.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        content = response.json()
        self.assertEqual(
            content['item'],
            ['The chosen item in the specified BIS List does not have the raid loot as its BIS.'],
        )

        data = {
            'greed': True,
            'greed_bis_id': self.tl_alt_bis2.pk,
            'item': 'body',
            'member_id': self.tl_tm.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        content = response.json()
        self.assertEqual(
            content['item'],
            ['The chosen item in the specified BIS List does not have the raid loot as its BIS.'],
        )

    def test_delete(self):
        """
        Attempt to delete Loot entries for a Team and ensure all the details play nicely
        """
        user = self._get_user()
        self.client.force_authenticate(user)
        url = reverse('api:loot_delete', kwargs={'team_id': self.team.pk})

        # Create some Loot entries for this Team, along with one for a new Team (just to make sure filtering works)
        other_team = Team.objects.create(
            invite_code=Team.generate_invite_code(),
            name='Les Jambons Deux',
            tier=Tier.objects.get(max_item_level=605),
        )
        other_team_member = other_team.members.create(character=self.main_tank, bis_list=self.mt_alt_bis, lead=True)
        l1 = Loot.objects.create(
            greed=False,
            item='mount',
            member=self.tl_tm,
            team=self.team,
            obtained=datetime.today(),
            tier=self.team.tier,
        )
        l2 = Loot.objects.create(
            greed=True,
            item='mainhand',
            member=self.mt_tm,
            team=self.team,
            obtained=datetime.today(),
            tier=self.team.tier,
        )
        l3 = Loot.objects.create(
            greed=False,
            item='body',
            member=self.mt_tm,
            team=self.team,
            obtained=datetime.today(),
            tier=self.team.tier,
        )
        l4 = Loot.objects.create(
            greed=False,
            item='body',
            member=other_team_member,
            team=other_team,
            obtained=datetime.today(),
            tier=self.team.tier,
        )

        body = {'items': [l1.pk, l3.pk, l4.pk]}
        response = self.client.post(url, body)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, response.content)
        with self.assertRaises(Loot.DoesNotExist):
            Loot.objects.get(pk=l1.pk)
        with self.assertRaises(Loot.DoesNotExist):
            Loot.objects.get(pk=l3.pk)
        Loot.objects.get(pk=l2.pk)
        Loot.objects.get(pk=l4.pk)

    def test_404(self):
        """
        Test 404 errors are returned for bad urls in each endpoint / method;

        - Invalid ID
        - Not having a character in the team
        - POST when not the team lead
        """
        user = self._get_user()
        self.client.force_authenticate(user)

        # Invalid ID
        url = reverse('api:loot_collection', kwargs={'team_id': 'abcde'})
        self.assertEqual(self.client.get(url).status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(self.client.post(url).status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(self.client.post(f'{url}delete/').status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(self.client.post(f'{url}bis/').status_code, status.HTTP_404_NOT_FOUND)

        # Not having a character in the team
        self.team_lead.user = self._create_user()
        self.team_lead.save()
        url = reverse('api:loot_collection', kwargs={'team_id': self.team.pk})
        self.assertEqual(self.client.get(url).status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(self.client.post(url).status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(self.client.post(f'{url}delete/').status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(self.client.post(f'{url}bis/').status_code, status.HTTP_404_NOT_FOUND)

        # POST while not team lead
        self.client.force_authenticate(self.main_tank.user)
        self.assertEqual(self.client.post(url).status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(self.client.post(f'{url}delete/').status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(self.client.post(f'{url}bis/').status_code, status.HTTP_404_NOT_FOUND)
