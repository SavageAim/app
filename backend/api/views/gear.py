"""
Just a view to get the list of all gear in the system
"""

# lib
from drf_spectacular.utils import extend_schema, inline_serializer, OpenApiParameter
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
# local
from api.models import Gear
from api.serializers import (
    GearSerializer,
)


class GearCollection(APIView):
    """
    Get a list of Gears in the system
    """
    queryset = Gear
    serializer_class = GearSerializer(many=True)

    permission_classes = [AllowAny]

    @extend_schema(
        parameters=[
            OpenApiParameter('item_level_min', int, description='Set a minimum item level (inclusive) of Gear returned.'),
            OpenApiParameter('item_level_max', int, description='Set a maximum item level (inclusive) of Gear returned.'),
        ],
        operation_id='gear_list',
    )
    def get(self, request: Request) -> Response:
        """
        Retrieve a list of Gear objects from the system.
        """
        objs = Gear.objects.all()

        # Get the filters from the query parameters
        low_bound = request.query_params.get('item_level_min', None)
        high_bound = request.query_params.get('item_level_max', None)

        if low_bound is not None:
            try:
                objs = objs.filter(item_level__gte=low_bound)
            except ValueError:
                pass

        if high_bound is not None:
            try:
                objs = objs.filter(item_level__lte=high_bound)
            except ValueError:
                pass

        data = GearSerializer(objs, many=True).data
        return Response(data)


class ItemLevels(APIView):
    """
    Get the min and max values of item level currently in the system
    """

    permission_classes = [AllowAny]

    @extend_schema(
        responses={
            200: inline_serializer('ItemLevels', {'min': serializers.IntegerField(), 'max': serializers.IntegerField()}),
        },
        operation_id='read_item_level_range',
    )
    def get(self, request: Request) -> Response:
        """
        Retrieve the minimum and maximum Item Levels in the entire DB.
        """
        objs = Gear.objects.values('item_level')

        min_il = objs.last()['item_level']
        max_il = objs.first()['item_level']

        return Response({'min': min_il, 'max': max_il})
