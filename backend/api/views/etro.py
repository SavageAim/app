"""
Given an etro id, convert it into a format that uses Savage Aim ids
"""
# stdlib
from typing import Dict, Set, Tuple
# lib
import coreapi
import jellyfish
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
# local
from api.models import Gear


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
ARMOUR_SLOTS = {'head', 'body', 'hands', 'legs', 'feet'}
ACCESSORY_SLOTS = {'earrings', 'necklace', 'bracelet', 'left_ring', 'right_ring'}


class EtroImport(APIView):
    """
    Import an etro gearset using coreapi and levenshtein distance
    """

    @staticmethod
    def _get_gear_id(gear_selection: Dict[str, str], item_name: str) -> str:
        """
        Find the id of the gear piece that matches the name closest
        """
        diff = float('inf')
        gear_id = None
        for details in gear_selection:
            curr_diff = jellyfish.levenshtein_distance(details['name'], item_name)
            if curr_diff < diff:
                diff = curr_diff
                gear_id = details['id']
        return gear_id

    def get(self, request: Request, id: str) -> Response:
        """
        Return a list of Characters belonging to a certain User
        """
        # Instantiate a Client instance for CoreAPI
        client = coreapi.Client()
        schema = client.get("https://etro.gg/api/docs/")

        # First things first, attempt to read the gearset
        try:
            response = client.action(schema, ['gearsets', 'read'], params={'id': id})
        except coreapi.exceptions.ErrorMessage as e:
            return Response({'message': e.error.title}, status=400)
        job_id = response['jobAbbrev']

        # Loop through each slot of the etro gearset, fetch the name and item level and store it in a dict
        gear_details: Dict[str, str] = {}
        item_levels: Set[int] = set()

        for etro_slot, sa_slot in SLOT_MAP.items():
            gear_id = response[etro_slot]
            if gear_id is None:
                continue
            item_response = client.action(schema, ['equipment', 'read'], params={'id': gear_id})
            gear_details[sa_slot] = item_response['name']
            item_levels.add(item_response['itemLevel'])

        # Get the names of all the gear with the specified Item Levels
        gear_names = Gear.objects.filter(item_level__in=item_levels).values('name', 'id')

        response = {
            'job_id': job_id,
        }

        # Loop through the slots one final time, and get the gear id for that slot
        for slot, item_name in gear_details.items():
            if slot in ARMOUR_SLOTS:
                response[slot] = self._get_gear_id(gear_names.filter(has_armour=True), item_name)
            elif slot in ACCESSORY_SLOTS:
                response[slot] = self._get_gear_id(gear_names.filter(has_accessories=True), item_name)
            else:
                response[slot] = self._get_gear_id(gear_names.filter(has_weapon=True), item_name)

        # Check for offhand
        if job_id != 'PLD':
            response['offhand'] = response['mainhand']

        # Also add item level status
        response['min_il'] = min(*item_levels)
        response['max_il'] = max(*item_levels)

        return Response(response)
