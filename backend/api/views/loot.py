"""
Team Loot Views

Get the loot history and required for a Team.
Record new loot and update BIS Lists accordingly.
"""
# stdlib
from typing import Dict, List
from datetime import datetime
# lib
from django.core.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
# local
from .base import APIView
from api import notifier
from api.models import BISList, Loot, Team
from api.serializers import (
    LootSerializer,
    LootCreateSerializer,
    LootCreateWithBISSerializer,
    TeamSerializer,
)

PERMISSION_NAME = 'loot_manager'


class LootCollection(APIView):
    """
    Management of Team Loot
    """

    # These are the slots we can basically automate
    AUTOMATED_SLOTS = [
        'mainhand',
        'head',
        'body',
        'hands',
        'legs',
        'feet',
        'earrings',
        'necklace',
        'bracelet',
    ]
    # Offhand and Rings cannot be automated due to special handling
    NON_AUTOMATED_SLOTS = [
        'ring',
        'tome-accessory-augment',
        'tome-armour-augment'
    ]

    def _get_gear_data(self, obj: Team) -> Dict[str, List[Dict[str, str]]]:
        """
        An attempt at improving the original loot response with less DB hits + waiting required.
        """
        # Set up the whole response dictionary at once
        response = {slot: {'need': [], 'greed': []} for slot in self.AUTOMATED_SLOTS}
        for slot in self.NON_AUTOMATED_SLOTS:
            response[slot] = {'need': [], 'greed': []}

        # Maintain a mapping of character greed lists
        greed_lists = {}

        raid_gear_name = obj.tier.raid_gear_name

        # Loop through every member of the team.
        for member in obj.members.all():
            greed_lists[member.id] = {}
            # Loop through the member's greed BIS Lists
            for bis_list in BISList.objects.with_all_relations().filter(owner=member.character):
                for slot in self.AUTOMATED_SLOTS:
                    greed_lists[member.id].setdefault(slot, [])

                    list_is_need = bis_list.id == member.bis_list_id
                    bis = getattr(bis_list, f'bis_{slot}')
                    current = getattr(bis_list, f'current_{slot}')

                    if bis.name == raid_gear_name and current.name != raid_gear_name:
                        if list_is_need:
                            response[slot]['need'].append({
                                'member_id': member.id,
                                'character_name': member.character.display_name,
                                'current_gear_name': current.name,
                                'current_gear_il': current.item_level,
                                'job_icon_name': bis_list.job.id,
                                'job_role': bis_list.job.role,
                            })
                        else:
                            greed_lists[member.id][slot].append({
                                'bis_list_name': bis_list.display_name,
                                'bis_list_id': bis_list.id,
                                'current_gear_name': current.name,
                                'current_gear_il': current.item_level,
                                'job_icon_name': bis_list.job.id,
                                'job_role': bis_list.job.role,
                            })

                # For non-automated slots we have to do stuff more manually
                slot = 'ring'
                greed_lists[member.id].setdefault(slot, [])

                bis_ring_check = [
                    bis_list.bis_right_ring.name == raid_gear_name,
                    bis_list.bis_left_ring.name == raid_gear_name,
                ]
                current_ring_check = [
                    bis_list.current_right_ring.name != raid_gear_name,
                    bis_list.current_left_ring.name != raid_gear_name,
                ]
                if any(bis_ring_check) and all(current_ring_check):
                    if list_is_need:
                        response[slot]['need'].append({
                            'member_id': member.id,
                            'character_name': member.character.display_name,
                            'current_gear_name': current.name,
                            'current_gear_il': current.item_level,
                            'job_icon_name': bis_list.job.id,
                            'job_role': bis_list.job.role,
                        })
                    else:
                        greed_lists[member.id][slot].append({
                            'bis_list_name': bis_list.display_name,
                            'bis_list_id': bis_list.id,
                            'current_gear_name': current.name,
                            'current_gear_il': current.item_level,
                            'job_icon_name': bis_list.job.id,
                            'job_role': bis_list.job.role,
                        })

                slot = 'tome-accessory-augment'
                greed_lists[member.id].setdefault(slot, [])
                required = bis_list.accessory_augments_required(obj.tier.tome_gear_name)
                if required > 0:
                    if list_is_need:
                        response[slot]['need'].append({
                            'member_id': member.id,
                            'character_name': member.character.display_name,
                            'job_icon_name': member.bis_list.job.id,
                            'job_role': member.bis_list.job.role,
                            'requires': required,
                        })
                    else:
                        greed_lists[member.id][slot].append({
                            'bis_list_name': bis_list.display_name,
                            'bis_list_id': bis_list.id,
                            'job_icon_name': bis_list.job.id,
                            'job_role': bis_list.job.role,
                            'requires': required,
                        })

                slot = 'tome-armour-augment'
                greed_lists[member.id].setdefault(slot, [])
                required = bis_list.armour_augments_required(obj.tier.tome_gear_name)
                if required > 0:
                    if list_is_need:
                        response[slot]['need'].append({
                            'member_id': member.id,
                            'character_name': member.character.display_name,
                            'job_icon_name': member.bis_list.job.id,
                            'job_role': member.bis_list.job.role,
                            'requires': required,
                        })
                    else:
                        greed_lists[member.id][slot].append({
                            'bis_list_name': bis_list.display_name,
                            'bis_list_id': bis_list.id,
                            'job_icon_name': bis_list.job.id,
                            'job_role': bis_list.job.role,
                            'requires': required,
                        })

        # Lastly, consolidate the two storages of items into one
        for member in obj.members.all():
            for slot in greed_lists[member.id]:
                response[slot]['greed'].append({
                    'member_id': member.id,
                    'character_name': member.character.display_name,
                    'greed_lists': greed_lists[member.id][slot],
                })

        return response

    def get(self, request: Request, team_id: str) -> Response:
        """
        Get loot history and current need/greed status for a team
        """
        try:
            obj = Team.objects.select_related(
                'tier',
            ).prefetch_related(
                'members',
                'members__character',
                'members__bis_list',
            ).get(pk=team_id, members__character__user=request.user)
        except (Team.DoesNotExist, ValidationError):
            return Response(status=404)

        # Getting the list of Loot for the current tier is easy
        objs = Loot.objects.filter(team=obj, tier=obj.tier)
        history = LootSerializer(objs, many=True).data

        # Get the gear information from the above hidden function
        gear = self._get_gear_data(obj)

        # Build and return the response
        loot_data = {'gear': gear, 'history': history}
        team_data = TeamSerializer(obj).data
        return Response({'team': team_data, 'loot': loot_data})

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
