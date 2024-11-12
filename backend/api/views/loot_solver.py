"""
Team Loot Views

Get the loot history and required for a Team.
Record new loot and update BIS Lists accordingly.
"""
# stdlib
from collections import defaultdict, deque
from copy import deepcopy
from typing import Dict, List, Tuple, Union
# lib
from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from drf_spectacular.utils import inline_serializer
from drf_spectacular.views import extend_schema
from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
# local
from .base import APIView
from api.models import Gear, Job, Loot, Settings, Team, TeamMember, Tier

Requirements = Dict[str, List[int]]
PrioBrackets = Dict[int, List[int]]
HandoutData = Dict[str, Union[str, bool, None]]
NonLootGear = Dict[int, List[str]]


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

    FIRST_FLOOR_SLOTS = ['earrings', 'necklace', 'bracelet', 'ring']
    SECOND_FLOOR_SLOTS = ['head', 'hands', 'feet', 'tome-accessory-augment']
    THIRD_FLOOR_SLOTS = ['body', 'legs', 'tome-armour-augment', ]
    FIRST_FLOOR_TOKENS = 3
    SECOND_FLOOR_TOKENS = 3
    THIRD_FLOOR_TOKENS = 4

    @staticmethod
    def _get_current_member_priority(prio_brackets: PrioBrackets, member_id: int) -> int:
        """
        Find what priority the given member has in the given prio brackets.
        Returns 0 if they are not in the prio brackets
        """
        for prio, members in prio_brackets.items():
            if member_id in members:
                return prio
        return 0

    @staticmethod
    def _get_team_solver_sort_order(team: Team) -> List[int]:
        """
        Given a Team, apply their solver sort overrides to the default list, then turn that new list into a list of member IDs.
        """
        overrides = team.solver_sort_overrides
        remaining_default_order = deque(Job.get_in_solver_order().exclude(id__in=overrides).values_list('id', flat=True))
        positions = {v - 1: k for k, v in overrides.items()}
        total_jobs = len(overrides) + len(remaining_default_order)
        job_order = deque()
        for i in range(total_jobs):
            if i in positions:
                job_order.append(positions[i])
            else:
                job_order.append(remaining_default_order.popleft())

        # Turn our ordered Job list into the list of team members ordered by the given sort order
        member_jobs = {
            member.pk: member.bis_list.job.id
            for member in team.members.all()
        }
        return sorted(member_jobs, key=lambda member_id: job_order.index(member_jobs[member_id]))

    @staticmethod
    def _get_requirements_map(team: Team) -> Requirements:
        """
        Scan the team's loot info and build a map of { item: [ids, of, people, who, need, it] }
        Note that this method builds up the overall map. The items already handed out are filtered out by _get_floor_data!
        """
        # Build the mapping of who needs what so we can pass that to the functions
        tier: Tier = team.tier
        requirements: Requirements = defaultdict(list)
        for member in team.members.all():
            for slot_name in LootSolver.SLOTS:
                required_slot = slot_name if '_ring' not in slot_name else 'ring'
                bis_slot: Gear = getattr(member.bis_list, f'bis_{slot_name}')

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
    def _get_gear_not_obtained_from_drops(tier: Tier, members: List[TeamMember], history: QuerySet[Loot]) -> NonLootGear:
        """
        Check for each Member in the Team for any loot they received that wasn't through drops
        """
        history_info = history.values_list('member_id', 'item')
        loot_gear = defaultdict(list)
        for (member_id, item) in history_info:
            loot_gear[member_id].append(item)

        non_loot_gear: Dict[int, List[str]] = {}
        for member in members:
            member_bis_gear = []
            for slot_name in LootSolver.SLOTS:
                required_slot = slot_name if '_ring' not in slot_name else 'ring'
                bis_slot: Gear = getattr(member.bis_list, f'bis_{slot_name}')
                current_slot: Gear = getattr(member.bis_list, f'current_{slot_name}')

                if bis_slot.id != current_slot.id:
                    continue

                if bis_slot.name == tier.raid_gear_name:
                    member_bis_gear.append(required_slot)
                elif bis_slot.name == tier.tome_gear_name:
                    # Check what augment item is needed
                    if slot_name in LootSolver.ARMOUR:
                        token = 'tome-armour-augment'
                    elif slot_name in LootSolver.ACCESSORIES:
                        token = 'tome-accessory-augment'
                    else:
                        # Shouldn't happen since mainhand bis will ALWAYS be raid weapon
                        continue
                    member_bis_gear.append(token)

            # Remove the stuff they got through the history
            for history_item in loot_gear[member.id]:
                try:
                    member_bis_gear.remove(history_item)
                except ValueError:
                    # They haven't updated their list ;-;
                    pass
            non_loot_gear[member.id] = member_bis_gear
        return non_loot_gear

    @staticmethod
    def _get_floor_data(
        requirements: Requirements,
        history: QuerySet[Loot],
        slots: List[str],
        id_order: List[int],
        non_loot_gear: NonLootGear,
    ) -> Tuple[int, PrioBrackets, Requirements]:
        """
        Turn a requirements map and history into the priority bracket information, along with how many clears have already been recorded for the fight.
        Also generate and return the updated Requirements from the Loot History
        """
        # Limit floor requirements to the items that were important, then remove from this list as we update the prios below
        floor_requirements = {
            slot: requirements.get(slot, [])
            for slot in slots
        }
        relevant_history = history.filter(item__in=slots).order_by('obtained')
        clears = len({item.obtained for item in relevant_history})
        prio_brackets = LootSolver._generate_priority_brackets(floor_requirements, id_order)

        # Sim through the existing clear data and update prio brackets with how things have evolved in the past
        history_data: Dict[str, Dict[str, List[int]]] = defaultdict(lambda: defaultdict(list))
        for item in relevant_history:
            # Use a list so we can potentially handle split clears?
            history_data[item.obtained][item.item].append(item.member_id)

        for obtained in history_data:
            for slot in slots:
                for member_id in history_data[obtained].get(slot, []):
                    # move the receiver of the item down one bracket, making a new one if you have to
                    for priority in sorted(prio_brackets, reverse=True):
                        try:
                            prio_brackets[priority].remove(member_id)
                            try:
                                floor_requirements[slot].remove(member_id)
                            except ValueError:
                                pass
                            if prio_brackets[priority] == []:
                                prio_brackets.pop(priority)

                            # Sanity Check; don't add 0 prio (or anything lower) to the list
                            new_prio = priority - 1
                            if new_prio <= 0:
                                continue

                            if new_prio not in prio_brackets:
                                prio_brackets[new_prio] = [member_id]
                            else:
                                prio_brackets[new_prio].append(member_id)
                            break
                        except ValueError:
                            # If they're not in the prio bracket at this prio just keep going
                            continue

        # Also check loot not tracked in the history
        for member_id in id_order:
            # Go through the slots, if they're in the requirements map, remove the user from them and move them down a prio
            for non_loot_item in non_loot_gear.get(member_id, []):
                if non_loot_item not in floor_requirements:
                    continue

                for priority in sorted(prio_brackets, reverse=True):
                    try:
                        prio_brackets[priority].remove(member_id)
                        try:
                            floor_requirements[non_loot_item].remove(member_id)
                        except ValueError:
                            pass

                        if prio_brackets[priority] == []:
                            prio_brackets.pop(priority)

                        # Sanity Check; don't add 0 prio (or anything lower) to the list
                        new_prio = priority - 1
                        if new_prio <= 0:
                            continue

                        if new_prio not in prio_brackets:
                            prio_brackets[new_prio] = [member_id]
                        else:
                            prio_brackets[new_prio].append(member_id)
                        break
                    except ValueError:
                        # If they're not in the prio bracket at this prio just keep going
                        continue

        # Remove the 0 key
        prio_brackets.pop(0, None)
        return clears, prio_brackets, floor_requirements

    @staticmethod
    def _get_output_slot_name(slot: str) -> str:
        return slot.replace('-', ' ').title()

    @staticmethod
    def _get_handout_data(slots: List[str], requirements: Requirements, prio_brackets: PrioBrackets, weeks_per_token: int, weeks: int, greedy: bool = False) -> List[HandoutData]:
        """
        Do the algorithm for gathering handout information
        """
        handouts = []
        remove_slots = slots.copy()
        # Deepcopy the prio brackets dict so that sentry errors can print the upper level prio brackets for more debugging ease
        prio_brackets = deepcopy(prio_brackets)
        if 'augment' in slots[-1]:
            remove_slots = [remove_slots[-1]]
        while len(prio_brackets) > 0:
            weeks += 1
            week_data = {}

            # Check what items we no longer need this week and add them to the handout info
            for slot, needs in requirements.items():
                if len(needs) == 0:
                    week_data[LootSolver._get_output_slot_name(slot)] = None

            # Build up a map of who is needed to sort every required item for the week
            required_slots_for_week = set(slot for slot in requirements if LootSolver._get_output_slot_name(slot) not in week_data)
            needed_item_count = len(required_slots_for_week)

            # Loop through the people in priority order, populating a map of who needs what until all of the required items for the week are covered
            # This ensures each item is given to the person with the highest priority of getting it
            done = False
            potential_loot_members: Dict[int, List[str]] = {}
            for priority in sorted(prio_brackets, reverse=True):
                for member_id in prio_brackets[priority]:
                    required = [slot for slot in requirements if member_id in requirements[slot]]
                    potential_loot_members[member_id] = required

                    # Subtract from the set of things needed this week
                    required_slots_for_week -= set(required)

                    # Check that we have enough potential members to cover each available item
                    if len(potential_loot_members) >= needed_item_count and len(required_slots_for_week) == 0:
                        done = True
                        break
                if done:
                    break

            # At this point, we have a mapping of potential member_ids to the items they still need this week.
            # It has the minimum required amount of people such that every Need item can be handed out to someone.
            # Now we determine who actually gets what
            # There is a 3 step priority system to sorting out handouts;
            # 1 - Anyone who has only one potential item
            # 2 - Anyone who is the only person who needs a given item
            # 3 - Go down the list from highest to lowest priority and just give them one of the needed items
            # Whenever we give someone an item, we remove them from the potential list, remove their item from everyone elses'
            # If anyone gets reduced to 1 item left, they get added to the queue
            handout_queue = deque()

            # Handle the two special cases first
            # 1 - Anyone who only has 1 item they can get
            for member_id, member_items in potential_loot_members.items():
                if len(member_items) == 1:
                    handout_queue.append((member_id, member_items[0]))

            # 2 - Anyone who has a unique item in their list
            for member_id, member_items in potential_loot_members.items():
                member_items_set = set(member_items)
                other_set = set()
                for other_member_id, other_member_items in potential_loot_members.items():
                    if member_id == other_member_id:
                        continue
                    other_set |= set(other_member_items)

                uniques = member_items_set - other_set
                for unique_item in uniques:
                    handout_queue.append((member_id, unique_item))

            # Loop until we get all the requirements
            while len(week_data) < len(requirements) and (len(potential_loot_members) > 0 or len(handout_queue) > 0):
                # Check if we've already had someone in the handout queue, if not we get the first id and item
                if len(handout_queue) > 0:
                    member_id, item = handout_queue.popleft()
                else:
                    member_id = list(potential_loot_members)[0]
                    member_items = potential_loot_members.get(member_id, [])
                    if len(member_items) == 0:
                        # Remove the member and re-loop
                        potential_loot_members.pop(member_id, None)
                        continue
                    item = member_items[0]

                # Attempt to give this item to the chosen member, if it's not already in the week's data
                output_item_name = LootSolver._get_output_slot_name(item)
                if output_item_name in week_data:
                    continue

                # Check if we're already at the end of needing to assign loot
                member_items_left = LootSolver._get_current_member_priority(prio_brackets, member_id)
                if greedy and weeks % weeks_per_token == 0 and item in remove_slots and member_items_left <= 1:
                    week_data[output_item_name] = None
                    continue

                # At this point, the item is guaranteed to go to this person
                week_data[output_item_name] = member_id
                requirements[item].remove(member_id)

                # Reduce the requirement number of the person and add them to the end of the list
                prio = None
                for check_prio, names in prio_brackets.items():
                    if member_id in names:
                        prio = check_prio
                        break
                new_prio = prio - 1
                prio_brackets[prio].remove(member_id)
                if prio_brackets[prio] == []:
                    # If this empties the list, destroy it
                    prio_brackets.pop(check_prio, None)
                if new_prio > 0:
                    # If the assignee's new prio (number of items they need) isn't 0, add them to the lower prio
                    if new_prio not in prio_brackets:
                        prio_brackets[new_prio] = []
                    prio_brackets[new_prio].append(member_id)

                # Now we need to remove the member_id from potentials, and also remove the item from anyone else
                potential_loot_members.pop(member_id, None)
                for other_member_id, other_member_items in potential_loot_members.items():
                    try:
                        other_member_items.remove(item)
                    except ValueError:
                        # If the item isn't in the list, that's fine
                        continue
                    if len(other_member_items) == 1:
                        # Put the person and their item into the queue
                        handout_queue.append((other_member_id, other_member_items[0]))

            # Add the week data to the handouts list
            handouts.append(week_data)

            # Lastly, if weeks % token_count == 0, reduce everyone's requirement by 1
            if weeks % weeks_per_token == 0:
                for priority in sorted(prio_brackets):
                    prio_brackets[priority - 1] = prio_brackets[priority]

                    # Need to also remove a loot item for everyone in the priority bracket to keep the requirements info in check
                    for member_id in prio_brackets[priority]:
                        # Reverse slots so that we always pop tokens if possible
                        for slot in remove_slots:
                            try:
                                requirements[slot].remove(member_id)
                                break
                            except ValueError:
                                # Keep searching until we find one
                                pass

                # Remove the 0 key and the highest key because that will have been duplicated
                prio_brackets.pop(0, None)
                try:
                    prio_brackets.pop(max(prio_brackets.keys()), None)
                except ValueError:
                    # 0 is also the max and we removed it?
                    pass
                week_data['token'] = True
            else:
                week_data['token'] = False

        return handouts

    def _get_first_floor_data(
        self,
        requirements: Requirements,
        history: QuerySet[Loot],
        id_order: List[int],
        non_loot_gear_obtained: NonLootGear,
        greedy: bool = False,
    ) -> List[HandoutData]:
        """
        Simulate handing out the loot for a first floor clear.
        """
        weeks, prio_brackets, floor_requirements = self._get_floor_data(
            requirements,
            history,
            self.FIRST_FLOOR_SLOTS,
            id_order,
            non_loot_gear_obtained,
        )
        return self._get_handout_data(self.FIRST_FLOOR_SLOTS, floor_requirements, prio_brackets, self.FIRST_FLOOR_TOKENS, weeks, greedy)

    @staticmethod
    def _get_second_floor_data(
        requirements: Requirements,
        history: QuerySet[Loot],
        id_order: List[int],
        non_loot_gear_obtained: NonLootGear,
        greedy: bool = False,
    ) -> List[HandoutData]:
        """
        Simulate handing out the loot for a second floor clear.
        """
        weeks, prio_brackets, floor_requirements = LootSolver._get_floor_data(
            requirements,
            history,
            LootSolver.SECOND_FLOOR_SLOTS,
            id_order,
            non_loot_gear_obtained,
        )
        return LootSolver._get_handout_data(LootSolver.SECOND_FLOOR_SLOTS, floor_requirements, prio_brackets, LootSolver.SECOND_FLOOR_TOKENS, weeks, greedy)

    def _get_third_floor_data(
        self,
        requirements: Requirements,
        history: QuerySet[Loot],
        id_order: List[int],
        non_loot_gear_obtained: NonLootGear,
        greedy: bool = False,
    ) -> List[HandoutData]:
        """
        Simulate handing out the loot for a third floor clear.
        """
        weeks, prio_brackets, floor_requirements = self._get_floor_data(
            requirements,
            history,
            self.THIRD_FLOOR_SLOTS,
            id_order,
            non_loot_gear_obtained,
        )
        return self._get_handout_data(self.THIRD_FLOOR_SLOTS, floor_requirements, prio_brackets, self.THIRD_FLOOR_TOKENS, weeks, greedy)

    def _get_fourth_floor_data(self, history: QuerySet[Loot], team_size: int, non_loot_gear_obtained: NonLootGear) -> HandoutData:
        """
        Simulate handing out the loot for a fourth floor clear.
        Different from how the others are handled, because we just check how many people already have bis weapon, and also how many mounts have been obtained.
        """
        weapons_obtained = history.filter(item='mainhand', greed=False).count()
        non_loot_weapons = len([member_id for member_id in non_loot_gear_obtained if 'mainhand' in non_loot_gear_obtained[member_id]])
        mounts_obtained = history.filter(item='mount').count()
        return {
            'weapons': team_size - weapons_obtained - non_loot_weapons,
            'mounts': team_size - mounts_obtained,
        }

    @extend_schema(
        tags=['team_loot'],
        responses={
            200: inline_serializer(
                'LootSolverResponse',
                {
                    'first_floor': inline_serializer(
                        'LootSolverFirstFloorResponse',
                        {
                            slot: serializers.IntegerField()
                            for slot in FIRST_FLOOR_SLOTS
                        },
                        many=True,
                    ),
                    'second_floor': inline_serializer(
                        'LootSolverSecondFloorResponse',
                        {
                            slot: serializers.IntegerField()
                            for slot in SECOND_FLOOR_SLOTS
                        },
                        many=True,
                    ),
                    'third_floor': inline_serializer(
                        'LootSolverThirdFloorResponse',
                        {
                            slot: serializers.IntegerField()
                            for slot in THIRD_FLOOR_SLOTS
                        },
                        many=True,
                    ),
                    'fourth_floor': inline_serializer(
                        'LootSolverFourthFloorResponse',
                        {
                            'weapons': serializers.IntegerField(),
                            'mounts': serializers.IntegerField(),
                        },
                    ),
                }
            )
        },
        operation_id='run_loot_solver',
    )
    def get(self, request: Request, team_id: str) -> Response:
        """
        Run the Loot Solver for the specified Team.

        The Loot Solver is a system that attempts to generate an ordering for each piece of loot every week,
        in order to attempt and finish gearing as fast as possible for each of the first three fights of a Tier.

        For the first three floors, each slot will have a list of TeamMember IDs in the order you should hand them out.
        For the final fight, it simply returns the number of Weapons and Mounts required.
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
            ).distinct().get(pk=team_id, members__character__user=request.user)
        except (Team.DoesNotExist, ValidationError):
            return Response(status=404)

        id_ordering = self._get_team_solver_sort_order(obj)

        # Generate the requirements map for the Team
        requirements = self._get_requirements_map(obj)

        # Gather the loot details for the Team so far so we can calculate things like mounts needed or how many clears have already happened
        history = Loot.objects.filter(team=obj, tier=obj.tier)

        # Determine what items were obtained by each member outside of drops from a fight (purchased / obtained elsewhere)
        non_loot_gear_obtained = self._get_gear_not_obtained_from_drops(obj.tier, obj.members.all(), history)

        # Run the four functions  gather them all up and build up a map for the response
        try:
            greedy = request.user.settings.loot_solver_greed
        except Settings.DoesNotExist:
            greedy = False
        first = self._get_first_floor_data(requirements, history, id_ordering, non_loot_gear_obtained, greedy)
        second = self._get_second_floor_data(requirements, history, id_ordering, non_loot_gear_obtained, greedy)
        third = self._get_third_floor_data(requirements, history, id_ordering, non_loot_gear_obtained, greedy)
        fourth = self._get_fourth_floor_data(history, obj.members.count(), non_loot_gear_obtained)

        # Build and return the response
        return Response({
            'first_floor': first,
            'second_floor': second,
            'third_floor': third,
            'fourth_floor': fourth,
        })
