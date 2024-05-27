"""
Team Loot Views

Get the loot history and required for a Team.
Record new loot and update BIS Lists accordingly.
"""
# stdlib
from collections import defaultdict, deque
from typing import Dict, List, Tuple, Union
# lib
from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from rest_framework.request import Request
from rest_framework.response import Response
# local
from .base import APIView
from api.models import Gear, Job, Loot, Team, TeamMember, Tier

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
    SECOND_FLOOR_TOKENS = 4
    THIRD_FLOOR_TOKENS = 4

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
    def _get_handout_data(slots: List[str], requirements: Requirements, prio_brackets: PrioBrackets, weeks_per_token: int, weeks: int) -> List[HandoutData]:
        """
        Do the algorithm for gathering handout information
        """
        handouts = []
        remove_slots = slots.copy()
        if 'augment' in slots[-1]:
            remove_slots = [remove_slots[-1]] + remove_slots[:-1]
        while len(prio_brackets) > 0:
            weeks += 1
            week_data = {'token': False}
            # Run through the slots
            for slot in slots:
                # Check the prio brackets in descending order
                assignee = None
                for check_prio in sorted(prio_brackets, reverse=True):
                    # Run through the names and find the highest prio assignee
                    for check_id in prio_brackets.get(check_prio, []):
                        if check_id in requirements.get(slot, []):
                            assignee = check_id
                            requirements[slot].remove(assignee)
                            break

                    if assignee is not None:
                        break
                week_data[slot.replace('-', ' ').title()] = assignee

                if assignee is None:
                    continue

                # Reduce the requirement number of the person and add them to the end of the list
                new_prio = check_prio - 1
                prio_brackets[check_prio].remove(assignee)
                if prio_brackets[check_prio] == []:
                    # If this empties the list, destroy it
                    prio_brackets.pop(check_prio, None)
                if new_prio > 0:
                    # If the assignee's new prio (number of items they need) isn't 0, add them to the lower prio
                    try:
                        prio_brackets[new_prio].append(assignee)
                    except KeyError:
                        # Defaultdict doesn't re-default if the list is removed
                        prio_brackets[new_prio] = [assignee]

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

        return handouts

    def _get_first_floor_data(
        self,
        requirements: Requirements,
        history: QuerySet[Loot],
        id_order: List[int],
        non_loot_gear_obtained: NonLootGear,
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
        return self._get_handout_data(self.FIRST_FLOOR_SLOTS, floor_requirements, prio_brackets, self.FIRST_FLOOR_TOKENS, weeks)

    @staticmethod
    def _get_second_floor_data(
        requirements: Requirements,
        history: QuerySet[Loot],
        id_order: List[int],
        non_loot_gear_obtained: NonLootGear,
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
        return LootSolver._get_handout_data(LootSolver.SECOND_FLOOR_SLOTS, floor_requirements, prio_brackets, LootSolver.SECOND_FLOOR_TOKENS, weeks)

    def _get_third_floor_data(
        self,
        requirements: Requirements,
        history: QuerySet[Loot],
        id_order: List[int],
        non_loot_gear_obtained: NonLootGear,
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
        return self._get_handout_data(self.THIRD_FLOOR_SLOTS, floor_requirements, prio_brackets, self.THIRD_FLOOR_TOKENS, weeks)

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

    def get(self, request: Request, team_id: str) -> Response:
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
        first = self._get_first_floor_data(requirements, history, id_ordering, non_loot_gear_obtained)
        second = self._get_second_floor_data(requirements, history, id_ordering, non_loot_gear_obtained)
        third = self._get_third_floor_data(requirements, history, id_ordering, non_loot_gear_obtained)
        fourth = self._get_fourth_floor_data(history, obj.members.count(), non_loot_gear_obtained)

        # Build and return the response
        return Response({
            'first_floor': first,
            'second_floor': second,
            'third_floor': third,
            'fourth_floor': fourth,
        })
