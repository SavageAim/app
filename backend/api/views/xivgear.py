"""
Given an etro id, convert it into a format that uses Savage Aim ids
"""
# stdlib
from typing import Dict
# lib
import requests
from drf_spectacular.utils import inline_serializer, OpenApiResponse, OpenApiParameter
from drf_spectacular.views import extend_schema
from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
# local
from api.models import Gear
from api.views.base import ImportAPIView
from api.xivapi_item_search_client import XIVAPISearchClient


# Map names of slots from etro to savage aim
SLOT_MAP = {
    'Weapon': 'mainhand',
    'OffHand': 'offhand',
    'Head': 'head',
    'Body': 'body',
    'Hand': 'hands',
    'Legs': 'legs',
    'Feet': 'feet',
    'Ears': 'earrings',
    'Neck': 'necklace',
    'Wrist': 'bracelet',
    'RingLeft': 'left_ring',
    'RingRight': 'right_ring',
}


class XIVGearImport(ImportAPIView):
    """
    Import an XIVGear set.
    """

    @extend_schema(
        parameters=[
            OpenApiParameter(
                'set',
                int,
                description='The set number to use if multiple are returned. Ignored if the ID is for a single set.',
            ),
        ],
        responses={
            200: OpenApiResponse(
                response=inline_serializer(
                    'XIVGearImportResponse',
                    {
                        'name': serializers.CharField(),
                        'job_id': serializers.CharField(),
                        'min_il': serializers.IntegerField(),
                        'max_il': serializers.IntegerField(),
                        'mainhand': serializers.IntegerField(),
                        'offhand': serializers.IntegerField(),
                        'head': serializers.IntegerField(),
                        'body': serializers.IntegerField(),
                        'hands': serializers.IntegerField(),
                        'legs': serializers.IntegerField(),
                        'feet': serializers.IntegerField(),
                        'earrings': serializers.IntegerField(),
                        'necklace': serializers.IntegerField(),
                        'bracelet': serializers.IntegerField(),
                        'right_ring': serializers.IntegerField(),
                        'left_ring': serializers.IntegerField(),
                    },
                ),
                description='Map of slot name to the IDs of the Gear objects that *should* match the item on the slot of the XIVGear set.'
            ),
            202: OpenApiResponse(
                response=inline_serializer(
                    'XIVGearSetChoiceRequired',
                    {
                        'name': serializers.CharField(),
                        'index': serializers.IntegerField(),
                    },
                    many=True,
                ),
                description='Returned when multiple sets were found and no valid `sets` query parameter was given. Provides details for the choice to be made.',
            ),
            400: OpenApiResponse(
                description='An error occurred on an external service. Error message from the service will be included in the response',
                response=inline_serializer('XIVGearImport400Response', {'message': serializers.CharField()}),
            ),
            404: OpenApiResponse(
                description='The provided id was not found on the XIVGear API.'
            ),
        },
        operation_id='import_gear_from_xivgear',
    )
    def get(self, request: Request, id: str) -> Response:
        """
        Attempt to load the information of an XIVGear Set, and turn it into information SavageAim can use.
        Names are mapped to Gear instances using name similarity, and is not 100% guaranteed to be correct.

        If there are multiple sets in the URL, specify the one you want with the query parameter.
        If no set has been specified, the set names will be returned for the User to pick one.
        """
        # Fetch the data for the given ID from XIVGear
        response = requests.get(f'https://api.xivgear.app/shortlink/{id}')
        if response.status_code == 404:
            return Response(status=404)
        if response.status_code != 200:
            return Response({'message': response.text}, status=400)
        response_data = response.json()
        job_id = response_data['job']

        # Check if the `sets` key is present, and if it is, determine which set we will be using
        items: Dict[str, Dict]
        imported_data = {'job_id': job_id}
        if 'sets' in response_data:
            sheet_sets = response_data['sets']
            if len(sheet_sets) == 1:
                items = sheet_sets[0]['items']
                imported_data['name'] = sheet_sets[0]['name']
            else:
                try:
                    set_index = int(request.query_params.get('set', -1))
                except ValueError:
                    return Response({'message': '`set` query parameter was not a valid number.'}, 400)

                if set_index not in range(len(sheet_sets)):
                    # Return the set names and indices for the user to pick one from
                    return Response(
                        [
                            {'name': set['name'], 'index': index}
                            for index, set in enumerate(sheet_sets)
                        ],
                        status=202,
                    )
                else:
                    items = sheet_sets[set_index]['items']
                    imported_data['name'] = sheet_sets[set_index]['name']
        else:
            items = response_data['items']
            imported_data['name'] = response_data['name']

        # Search through the items, building up a map of sa_slots to the item ids in XIVAPI
        sa_gear = {}
        for xg_slot, item_data in items.items():
            sa_gear[SLOT_MAP[xg_slot]] = item_data['id']

        # Pass the values of this map to the XIVAPISearchClient to get back all the names and ils
        try:
            gear_names = XIVAPISearchClient.get_item_information(*sa_gear.values())
        except requests.HTTPError as e:
            return Response({'message': e.response.text}, 400)

        if len(gear_names) != len(sa_gear):
            return Response({'message': 'Could not find some of the items on XIVAPI, please try again later!'}, 400)

        # Use the returned map to calculate the min and max ils, and also replace IDs with names in sa_gear
        min_il = float('inf')
        max_il = float('-inf')
        for slot, xivapi_id in list(sa_gear.items()):
            details = gear_names[xivapi_id]
            sa_gear[slot] = details['name']
            il = details['item_level']
            if il > max_il:
                max_il = il
            if il < min_il:
                min_il = il
        imported_data['min_il'] = min_il
        imported_data['max_il'] = max_il

        # Now we have min and max item levels, along with names for the gear, so we can start converting them.
        # Turn the names into SA gear ids
        gear_records = Gear.objects.filter(
            item_level__gte=min_il,
            item_level__lte=max_il,
        ).values('name', 'id', 'extra_import_classes', 'extra_import_names')

        # Loop through each gear slot and fetch the id based off the name
        for slot, item_name in sa_gear.items():
            if slot in self.ARMOUR_SLOTS:
                imported_data[slot] = self._get_gear_id(gear_records.filter(has_armour=True), item_name)
            elif slot in self.ACCESSORY_SLOTS:
                imported_data[slot] = self._get_gear_id(gear_records.filter(has_accessories=True), item_name)
            else:
                imported_data[slot] = self._get_gear_id(gear_records.filter(has_weapon=True), item_name)

        # Check for offhand
        if job_id != 'PLD':
            imported_data['offhand'] = imported_data['mainhand']

        return Response(imported_data)
