"""
Given a map of slot names to item names and levels, return a map of the slots to their corresponding Gear objects
"""
# stdlib
from typing import Dict
# lib
from drf_spectacular.views import extend_schema
from rest_framework.request import Request
from rest_framework.response import Response
# local
from api.models import Gear
from api.serializers import PluginImportSerializer, PluginImportResponseSerializer
from api.views.base import ImportAPIView


class PluginImport(ImportAPIView):
    """
    Convert names and item levels from in game items to Savage Aim Gear Items.
    """
    serializer_class = PluginImportResponseSerializer

    @extend_schema(
        request=PluginImportSerializer,
    )
    def post(self, request: Request) -> Response:
        """
        Given a set of names taken from in-game, turn the in-game names into the names and IDs of Gear records in the DB.
        This allows the plugin to send a valid update request using the official in-system Gear IDs.
        """
        # Use Serializer for validating the provided data
        serializer = PluginImportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Determine our max and min ils
        min_il = float('inf')
        max_il = float('-inf')
        for data in serializer.validated_data.values():
            item_level = data['item_level']
            if item_level < min_il:
                min_il = item_level
            if item_level > max_il:
                max_il = item_level

        gear_to_check = Gear.objects.filter(
            item_level__gte=min_il,
            item_level__lte=max_il,
        ).values('name', 'id', 'extra_import_names', 'extra_import_classes')

        response: Dict[str, Gear] = {}

        for slot, slot_data in serializer.validated_data.items():
            item_name, item_level = slot_data['name'], slot_data['item_level']
            if slot in self.ARMOUR_SLOTS:
                gear_id = self._get_gear_id(
                    gear_to_check.filter(has_armour=True, item_level=item_level),
                    item_name,
                )
            elif slot in self.ACCESSORY_SLOTS:
                gear_id = self._get_gear_id(
                    gear_to_check.filter(has_accessories=True, item_level=item_level),
                    item_name,
                )
            else:
                gear_id = self._get_gear_id(
                    gear_to_check.filter(has_weapon=True, item_level=item_level),
                    item_name,
                )

            try:
                if gear_id is None:
                    raise ValueError()
                response[slot] = gear_to_check.get(pk=gear_id)
            except (ValueError, Gear.DoesNotExist):
                response[slot] = None

        out_serializer = PluginImportResponseSerializer(response)
        return Response(out_serializer.data)
