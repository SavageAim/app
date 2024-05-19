"""
Team Loot Views

Get the loot history and required for a Team.
Record new loot and update BIS Lists accordingly.
"""
# stdlib
from collections import defaultdict
from datetime import datetime
from typing import Dict, List
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

PERMISSION_NAME = 'loot_manager'


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
    def _get_requirements_map(team: Team) -> Dict[str, List[int]]:
        """
        Scan the team's loot info and build a map of { item: [ids, of, people, who, need, it] }
        """
        # Build the mapping of who needs what so we can pass that to the functions
        tier: Tier = team.tier
        requirements: Dict[str, List[str]] = defaultdict(list)
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

    async def get(self, request: Request, team_id: str) -> Response:
        """
        Fetch the current solver information for the team
        """
        try:
            obj = Team.objects.select_related(
                'tier',
            ).prefetch_related(
                'members',
                'members__character',
                'members__character__bis_lists',
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

        requirements = self._get_requirements_map(obj)

        # Build and return the response
        return Response()

    def post(self, request: Request, team_id: str) -> Response:
        """
        Attempt to create new Loot entries.
        Any updates sent here will also update Character's BIS Lists
        """
        team = self._get_team_with_permission(request, team_id, PERMISSION_NAME)
        if team is None:
            return Response(status=404)

        # Firstly we validate the sent data
        serializer = LootCreateSerializer(data=request.data, context={'team': team})
        serializer.is_valid(raise_exception=True)
        serializer.save(team=team, tier=team.tier)

        # Send WS updates to the Team channel
        self._send_to_team(team, {'type': 'loot', 'id': str(team.id)})

        return Response({'id': serializer.instance.pk}, status=201)

    def delete(self, request: Request, team_id: str) -> Response:
        """
        Remove Loot entries from the Team's history.
        Entries to delete are specified in the request body.
        """
        team = self._get_team_with_permission(request, team_id, PERMISSION_NAME)
        if team is None:
            return Response(status=404)

        ids = request.data.get('items', [])
        Loot.objects.filter(team=team, pk__in=ids).delete()

        # Send WS updates to the Team channel
        self._send_to_team(team, {'type': 'loot', 'id': str(team.id)})

        return Response(status=204)


class LootWithBIS(APIView):
    """
    Create loot entries and also update BIS lists.
    Has stricter serializer since it affects two models instead of one
    """

    def post(self, request: Request, team_id: str) -> Response:
        """
        Attempt to create new Loot entries.
        Any updates sent here will also update Character's BIS Lists
        """
        team = self._get_team_with_permission(request, team_id, PERMISSION_NAME)
        if team is None:
            return Response(status=404)

        # Firstly we validate the sent data
        serializer = LootCreateWithBISSerializer(data=request.data, context={'team': team})
        serializer.is_valid(raise_exception=True)

        # If the data is valid, we want to create a Loot entry but also update some BIS Lists automagically.
        greed_bis_id = serializer.validated_data.pop('greed_bis_id', None)
        loot = Loot.objects.create(
            obtained=datetime.today(),
            team=team,
            tier=team.tier,
            **serializer.validated_data,
        )

        # Update BIS Lists
        list_id: int
        if serializer.validated_data['greed']:
            # Get the ID of BIS List to update
            list_id = greed_bis_id
        else:
            list_id = team.members.get(pk=serializer.validated_data['member_id']).bis_list_id

        item = serializer.validated_data['item']
        bis = BISList.objects.get(pk=list_id)
        # If it's ring, figure out which ring needs to be updated
        if item == 'ring':
            if bis.bis_right_ring.name == team.tier.raid_gear_name:
                item = 'right_ring'
            else:
                item = 'left_ring'
        # If we just copy bis_item onto current_item that will avoid any checking we have to do :D
        bis_item = getattr(bis, f'bis_{item}')
        setattr(bis, f'current_{item}', bis_item)
        if item == 'mainhand':
            # Set the offhand as well
            bis.current_offhand = bis_item
        bis.save()

        # Send a notification
        notifier.loot_tracker_update(bis, team)

        # Send WS updates to the Team channel
        self._send_to_team(team, {'type': 'loot', 'id': str(team.id)})

        return Response({'id': loot.pk}, status=201)
