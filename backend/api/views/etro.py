"""
Given an etro id, convert it into a format that uses Savage Aim ids
"""
# stdlib
from typing import Dict
# lib
import coreapi
from drf_spectacular.utils import inline_serializer, OpenApiResponse
from drf_spectacular.views import extend_schema
from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
# local
from api.models import Gear
from api.views.base import ImportAPIView


# Map names of slots from etro to savage aim
SLOT_MAP = {
    'weapon': 'mainhand',
    'offHand': 'offhand',
    'head': 'head',
    'body': 'body',
    'hands': 'hands',
    'legs': 'legs',
    'feet': 'feet',
    'ears': 'earrings',
    'neck': 'necklace',
    'wrists': 'bracelet',
    'fingerL': 'left_ring',
    'fingerR': 'right_ring',
}


class EtroImport(ImportAPIView):
    """
    Import an etro gearset using coreapi and levenshtein distance
    """

    @extend_schema(
        responses={
            200: OpenApiResponse(
                response=inline_serializer(
                    'EtroImportResponse',
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
                description='Map of slot name to the IDs of the Gear objects that *should* match the item on the slot of the Etro set.'
            ),
            400: OpenApiResponse(
                description='An error occurred on Etro\'s end. Error message from Etro will be included in the response',
                response=inline_serializer('EtroImport400Response', {'message': serializers.CharField()}),
            ),
        },
        operation_id='import_gear_from_etro',
    )
    def get(self, request: Request, id: str) -> Response:
        """
        Attempt to load the information of an Etro Gearset, and turn it into information SavageAim can use.

        Names are mapped to Gear instances using name similarity, and is not 100% guaranteed to be correct.
        """
        # Instantiate a Client instance for CoreAPI
        client = coreapi.Client()
        schema = client.get('https://etro.gg/api/docs/')

        # First things first, attempt to read the gearset
        try:
            gearset = client.action(schema, ['gearsets', 'read'], params={'id': id})
        except coreapi.exceptions.ErrorMessage as e:
            return Response({'message': e.error.title}, status=400)

        name = gearset['name']
        job_id = gearset['jobAbbrev']
        min_il = gearset['minItemLevel']
        max_il = gearset['maxItemLevel']

        # Retrieve a list of all gear within the item level bracket for the job
        params = {job_id: True, 'minItemLevel': min_il, 'maxItemLevel': max_il}
        equipment = client.action(schema, ['equipment', 'list'], params=params)
        # Map IDs to names
        etro_map = {
            item['id']: item['name'] for item in equipment
        }

        # Loop through the gear slots of the gear set and get the names for each
        gear_names: Dict[str, str] = {}
        for etro_slot, sa_slot in SLOT_MAP.items():
            gear_id = gearset[etro_slot]
            if gear_id is None:
                continue
            gear_names[sa_slot] = etro_map[gear_id]

        # Check for relic weapons
        if gearset['weapon'] is None and 'weapon' in gearset['relics']:
            relic_id = gearset['relics']['weapon']
            relic = client.action(schema, ['relic', 'read'], params={'id': relic_id})
            gear_names['mainhand'] = relic['baseItem']['name']

        # Turn the names into SA gear ids
        sa_gear = Gear.objects.filter(
            item_level__gte=min_il,
            item_level__lte=max_il,
        ).values('name', 'id', 'extra_import_classes', 'extra_import_names')
        response = {
            'name': name,
            'job_id': job_id,
            'min_il': min_il,
            'max_il': max_il,
        }

        # Loop through each gear slot and fetch the id based off the name
        for slot, item_name in gear_names.items():
            if slot in self.ARMOUR_SLOTS:
                response[slot] = self._get_gear_id(sa_gear.filter(has_armour=True), item_name)
            elif slot in self.ACCESSORY_SLOTS:
                response[slot] = self._get_gear_id(sa_gear.filter(has_accessories=True), item_name)
            else:
                response[slot] = self._get_gear_id(sa_gear.filter(has_weapon=True), item_name)

        # Check for offhand
        if job_id != 'PLD':
            response['offhand'] = response['mainhand']

        return Response(response)
