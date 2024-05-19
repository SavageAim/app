"""
Team Loot Views

Get the loot history and required for a Team.
Record new loot and update BIS Lists accordingly.
"""
# stdlib
import asyncio
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Tuple, Union
# lib
from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from rest_framework.request import Request
from rest_framework.response import Response
# local
from .base import APIView
from api import notifier
from api.models import BISList, Gear, Loot, Team, Tier
from api.serializers import (
    LootSerializer,
    LootCreateSerializer,
    LootCreateWithBISSerializer,
    TeamSerializer,
)

Requirements = Dict[str, List[int]]
PrioBrackets = Dict[int, List[int]]
HandoutData = Dict[str, Union[str, bool]]


class LootSolver(APIView):
    """
    Solve loot distribution to manage getting through a fight completely as fast as possible.
    """

    SLOTS = [
        'mainhand',
        'head',
        'body',
        'hands',
        'legs',
        'feet',
        'earrings',
        'necklace',
        'bracelet',
        'left_ring',
        'right_ring',
    ]

    ACCESSORIES = {'earrings', 'necklace', 'bracelet', 'right_ring', 'left_ring'}

    ARMOUR = {'head', 'body', 'hands', 'legs', 'feet'}

    FIRST_FLOOR_SLOTS = {'earrings', 'necklace', 'bracelet', 'ring'}
    SECOND_FLOOR_SLOTS = {'head', 'hands', 'feet', 'tome-accessory-augment'}
    THIRD_FLOOR_SLOTS = {'body', 'legs', 'tome-armour-augment'}

    def _get_gear_data(self, obj: Team) -> Dict[str, List[Dict[str, str]]]:
        """
        An attempt at improving the original loot response with less DB hits + waiting required.
        """
        pass

    def _get_history_loot_data(self, obj: Team, loot: QuerySet) -> Dict[str, List[Dict[str, str]]]:
        """
        A method for retrieving the loot items that are checked purely by the history data
        """
        pass

    @staticmethod
    def _get_requirements_map(team: Team) -> Requirements:
        """
        Scan the team's loot info and build a map of { item: [ids, of, people, who, need, it] }
        """
        # Build the mapping of who needs what so we can pass that to the functions
        tier: Tier = team.tier
        requirements: Requirements = defaultdict(list)
        for member in team.members.all():
            for slot_name in LootSolver.SLOTS:
                required_slot = slot_name if '_ring' not in slot_name else 'ring'
                bis_slot: Gear = getattr(member.bis_list, f'bis_{slot_name}')
                current_slot: Gear = getattr(member.bis_list, f'current_{slot_name}')

                # Skip if the person already has BIS
                if bis_slot.id == current_slot.id:
                    continue

                if bis_slot.name == tier.raid_gear_name:
                    requirements[required_slot].append(member.id)
                elif bis_slot.name == tier.tome_gear_name:
                    # Check what augment item is needed
                    if slot_name in LootSolver.ARMOUR:
                        token = 'tome-armour-augment'
                    elif slot_name in LootSolver.ACCESSORIES:
                        token = 'tome-accessory-augment'
                    else:
                        # Shouldn't happen since mainhand bis will ALWAYS be raid weapon
                        continue
                    requirements[token].append(member.id)
        return requirements

    @staticmethod
    def _generate_priority_brackets(requirements: Requirements, id_ordering: List[int]) -> PrioBrackets:
        """
        Given the requirements found by the above function, generate a new dictionary that gives priority brackets for items.
        This will be used by the individual floor functions that will want to use it on subsets of the overall requirements map.
        """
        # Firstly, turn data into map of ids to how many items they need
        items_needed = defaultdict(int)
        for ids in requirements.values():
            for id in ids:
                items_needed[id] += 1

        # Turn this into our prio bracket: name list with names sorted in required order
        prio_brackets = defaultdict(list)
        ordered_ids = sorted(items_needed, key=lambda id: id_ordering.index(id))
        for ids in ordered_ids:
            needed = items_needed[ids]
            prio_brackets[needed].append(ids)

        return dict(prio_brackets)
    
    @staticmethod
    def _get_floor_prio_and_clear_count(requirements: Requirements, history: QuerySet[Loot], slots: List[str]) -> Tuple[int, PrioBrackets]:
        """
        Turn a requirements map and history into the priority bracket information, along with how many clears have already been recorded for the fight.
        """
        floor_requirements = {
            slot: requirements.get(slot, [])
            for slot in slots
        }
        clears = len(set(history.filter(item__in=slots).values_list('item', flat=True)))
        return clears, floor_requirements

    async def _get_first_floor_data(self, requirements: Requirements, history: QuerySet[Loot], id_order: List[int]) -> List[HandoutData]:
        """
        Simulate handing out the loot for a first floor clear.
        """
        week, floor_requirements = self._get_floor_prio_and_clear_count(requirements, history, self.FIRST_FLOOR_SLOTS)
        


    async def get(self, request: Request, team_id: str) -> Response:
        """
        Fetch the current solver information for the team
        """
        try:
            obj = Team.objects.select_related(
                'tier',
            ).prefetch_related(
                'members',
                'members__bis_list',
                'members__bis_list__bis_body',
                'members__bis_list__bis_bracelet',
                'members__bis_list__bis_earrings',
                'members__bis_list__bis_feet',
                'members__bis_list__bis_hands',
                'members__bis_list__bis_head',
                'members__bis_list__bis_left_ring',
                'members__bis_list__bis_legs',
                'members__bis_list__bis_mainhand',
                'members__bis_list__bis_necklace',
                'members__bis_list__bis_offhand',
                'members__bis_list__bis_right_ring',
                'members__bis_list__current_body',
                'members__bis_list__current_bracelet',
                'members__bis_list__current_earrings',
                'members__bis_list__current_feet',
                'members__bis_list__current_hands',
                'members__bis_list__current_head',
                'members__bis_list__current_left_ring',
                'members__bis_list__current_legs',
                'members__bis_list__current_mainhand',
                'members__bis_list__current_necklace',
                'members__bis_list__current_offhand',
                'members__bis_list__current_right_ring',
                'members__bis_list__job',
            ).get(pk=team_id, members__character__user=request.user)
        except (Team.DoesNotExist, ValidationError):
            return Response(status=404)

        # Generate the ordering of IDs based on the decided pattern; DPS > Tanks > Healer
        # Natural DPS ordering is Melee > Ranged > Caster
        id_ordering = [
            *obj.members.filter(bis_list__job__role='dps').values_list('id', flat=True),
            *obj.members.filter(bis_list__job__role='tank').values_list('id', flat=True),
            *obj.members.filter(bis_list__job__role='heal').values_list('id', flat=True),
        ]

        # Generate the requirements map for the Team as it stands
        requirements = self._get_requirements_map(obj)

        # Gather the loot details for the Team so far so we can calculate things like mounts needed or how many clears have already happened
        history = Loot.objects.filter(team=obj, tier=obj.tier)

        # Run the four functions async, gather them all up and build up a map for the response
        first, second, third, fourth = asyncio.gather(
            self._get_first_floor_data(requirements, history, id_ordering),
            self._get_second_floor_data(requirements, history, id_ordering),
            self._get_third_floor_data(requirements, history, id_ordering),
            self._get_fourth_floor_data(requirements, history, id_ordering),
        )

        # Build and return the response
        return Response({
            'first_floor': first,
            'second_floor': second,
            'third_floor': third,
            'fourth_floor': fourth,
        })
