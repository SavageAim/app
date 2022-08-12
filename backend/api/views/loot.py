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
from django.db.models import Q
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

    # This could probably be done nice but /shrug for now
    def _get_gear_data(self, obj: Team) -> Dict[str, List[Dict[str, str]]]:
        """
        Generate and return the gear data
        Moving it to its own function so I can collapse it in my editor and not feel bad :)
        """
        # Calculating the list of need and greed is a little harder but should be okay
        gear = {}
        tier_name = obj.tier.raid_gear_name
        for slot in self.AUTOMATED_SLOTS:
            gear[slot] = {'need': [], 'greed': []}
            for tm in obj.members.all():
                # Check the Team linked BIS directly
                current_gear = getattr(tm.bis_list, f'current_{slot}')
                bis_name = getattr(tm.bis_list, f'bis_{slot}').name
                if current_gear.name != tier_name and bis_name == tier_name:
                    # Add details to the list
                    gear[slot]['need'].append({
                        'member_id': tm.id,
                        'character_name': tm.character.display_name,
                        'current_gear_name': current_gear.name,
                        'current_gear_il': current_gear.item_level,
                        'job_icon_name': tm.bis_list.job.id,
                        'job_role': tm.bis_list.job.role,
                    })

                # Get greed lists by doing a search on the character's other bis lists
                greed_lists = tm.character.bis_lists.select_related(
                    f'current_{slot}',
                    f'bis_{slot}',
                    'job',
                ).exclude(
                    **{f'current_{slot}__name': tier_name},
                ).filter(
                    **{f'bis_{slot}__name': tier_name},
                ).exclude(pk=tm.bis_list.id)
                data = {
                    'member_id': tm.id,
                    'character_name': tm.character.display_name,
                    'greed_lists': [],
                }
                for greed_list in greed_lists:
                    current_gear = getattr(greed_list, f'current_{slot}')
                    data['greed_lists'].append({
                        'bis_list_name': greed_list.display_name,
                        'bis_list_id': greed_list.id,
                        'current_gear_name': current_gear.name,
                        'current_gear_il': current_gear.item_level,
                        'job_icon_name': greed_list.job.id,
                        'job_role': greed_list.job.role,
                    })
                gear[slot]['greed'].append(data)

        # Now handle offhand and ring
        # slot = 'offhand'
        # gear[slot] = {'need': [], 'greed': []}
        # for tm in obj.members.all():
        #     # Check the Team linked BIS directly
        #     current_gear = getattr(tm.bis_list, 'current_offhand')
        #     bis_name = getattr(tm.bis_list, 'bis_offhand').name
        #     if current_gear.name != tier_name and bis_name == tier_name and tm.bis_list.job.id == 'PLD':
        #         # Add details to the list
        #         gear[slot]['need'].append({
        #             'member_id': tm.id,
        #             'character_name': tm.character.display_name,
        #             'current_gear_name': current_gear.name,
        #             'current_gear_il': current_gear.item_level,
        #             'job_icon_name': tm.bis_list.job.id,
        #             'job_role': tm.bis_list.job.role,
        #         })

        #     # Get greed lists by doing a search on the character's other bis lists
        #     greed_lists = tm.character.bis_lists.select_related(
        #         'current_offhand',
        #         'bis_offhand',
        #         'job',
        #     ).exclude(
        #         current_offhand__name=tier_name,
        #     ).filter(
        #         job_id='PLD',
        #         bis_offhand__name=tier_name,
        #     ).exclude(pk=tm.bis_list.id)
        #     data = {
        #         'member_id': tm.id,
        #         'character_name': tm.character.display_name,
        #         'greed_lists': [],
        #     }
        #     for greed_list in greed_lists:
        #         current_gear = getattr(greed_list, 'current_offhand')
        #         data['greed_lists'].append({
        #             'bis_list_name': greed_list.display_name,
        #             'bis_list_id': greed_list.id,
        #             'current_gear_name': current_gear.name,
        #             'current_gear_il': current_gear.item_level,
        #             'job_icon_name': greed_list.job.id,
        #             'job_role': greed_list.job.role,
        #         })
        #     gear[slot]['greed'].append(data)

        slot = 'ring'
        gear[slot] = {'need': [], 'greed': []}
        for tm in obj.members.all():
            # Determine which ring we need to check
            if tm.bis_list.bis_right_ring.name == tier_name:
                current_gear = tm.bis_list.current_right_ring
                bis_name = tm.bis_list.bis_right_ring.name
            else:
                current_gear = tm.bis_list.current_left_ring
                bis_name = tm.bis_list.bis_left_ring.name

            # Check the Team linked BIS directly
            if current_gear.name != tier_name and bis_name == tier_name:
                # Add details to the list
                gear[slot]['need'].append({
                    'member_id': tm.id,
                    'character_name': tm.character.display_name,
                    'current_gear_name': current_gear.name,
                    'current_gear_il': current_gear.item_level,
                    'job_icon_name': tm.bis_list.job.id,
                    'job_role': tm.bis_list.job.role,
                })

            # Get greed lists by doing a search on the character's other bis lists
            greed_lists = tm.character.bis_lists.select_related(
                'current_left_ring',
                'bis_left_ring',
                'current_right_ring',
                'bis_right_ring',
                'job',
            ).exclude(
                Q(current_left_ring__name=tier_name) | Q(current_right_ring__name=tier_name),
            ).filter(
                Q(bis_left_ring__name=tier_name) | Q(bis_right_ring__name=tier_name),
            ).exclude(pk=tm.bis_list.id)
            data = {
                'member_id': tm.id,
                'character_name': tm.character.display_name,
                'greed_lists': [],
            }
            for greed_list in greed_lists:
                # Determine which ring we need to use
                if greed_list.bis_right_ring.name == tier_name:
                    current_gear = greed_list.current_right_ring
                else:
                    current_gear = greed_list.current_left_ring

                data['greed_lists'].append({
                    'bis_list_name': greed_list.display_name,
                    'bis_list_id': greed_list.id,
                    'current_gear_name': current_gear.name,
                    'current_gear_il': current_gear.item_level,
                    'job_icon_name': greed_list.job.id,
                    'job_role': greed_list.job.role,
                })
            gear[slot]['greed'].append(data)

        # Tome augment tokens
        slot = 'tome-accessory-augment'
        gear[slot] = {'need': [], 'greed': []}
        for tm in obj.members.all():
            # Check the Team linked BIS directly
            needs = tm.bis_list.accessory_augments_required(obj.tier.tome_gear_name)
            if needs > 0:
                # Add details to the list
                gear[slot]['need'].append({
                    'member_id': tm.id,
                    'character_name': tm.character.display_name,
                    'job_icon_name': tm.bis_list.job.id,
                    'job_role': tm.bis_list.job.role,
                    'requires': needs,
                })

            # Get greed lists by doing a search on the character's other bis lists
            greed_lists = BISList.needs_accessory_augments(obj.tier.tome_gear_name).filter(
                owner=tm.character,
            ).exclude(pk=tm.bis_list.id)
            data = {
                'member_id': tm.id,
                'character_name': tm.character.display_name,
                'greed_lists': [],
            }
            for greed_list in greed_lists:
                data['greed_lists'].append({
                    'bis_list_name': greed_list.display_name,
                    'bis_list_id': greed_list.id,
                    'job_icon_name': greed_list.job.id,
                    'job_role': greed_list.job.role,
                    'requires': greed_list.accessory_augments_required(obj.tier.tome_gear_name),
                })
            gear[slot]['greed'].append(data)

        slot = 'tome-armour-augment'
        gear[slot] = {'need': [], 'greed': []}
        for tm in obj.members.all():
            # Check the Team linked BIS directly
            needs = tm.bis_list.armour_augments_required(obj.tier.tome_gear_name)
            if needs > 0:
                # Add details to the list
                gear[slot]['need'].append({
                    'member_id': tm.id,
                    'character_name': tm.character.display_name,
                    'job_icon_name': tm.bis_list.job.id,
                    'job_role': tm.bis_list.job.role,
                    'requires': needs,
                })

            # Get greed lists by doing a search on the character's other bis lists
            greed_lists = BISList.needs_armour_augments(obj.tier.tome_gear_name).filter(
                owner=tm.character,
            ).exclude(pk=tm.bis_list.id)
            data = {
                'member_id': tm.id,
                'character_name': tm.character.display_name,
                'greed_lists': [],
            }
            for greed_list in greed_lists:
                data['greed_lists'].append({
                    'bis_list_name': greed_list.display_name,
                    'bis_list_id': greed_list.id,
                    'job_icon_name': greed_list.job.id,
                    'job_role': greed_list.job.role,
                    'requires': greed_list.armour_augments_required(obj.tier.tome_gear_name),
                })
            gear[slot]['greed'].append(data)
        return gear

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
