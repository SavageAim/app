"""
Just a view to get the list of all gear in the system
"""

# lib
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

    permission_classes = [AllowAny]

    def get(self, request: Request) -> Response:
        """
        List the Gear items.

        We should allow filtering by item levels, both gte and lte
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

    def get(self, request: Request) -> Response:
        """
        Fetch the min and max item level for the system
        """
        objs = Gear.objects.values('item_level')

        min_il = objs.last()['item_level']
        max_il = objs.first()['item_level']

        return Response({'min': min_il, 'max': max_il})
