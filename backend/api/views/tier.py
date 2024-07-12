"""
Just a view to get the list of all tiers in the system
"""

# lib
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
# local
from api.models import Tier
from api.serializers import (
    TierSerializer,
)


class TierCollection(APIView):
    """
    Get a list of Tiers in the system
    """
    queryset = Tier
    serializer_class = TierSerializer(many=True)
    permission_classes = [AllowAny]

    def get(self, request: Request) -> Response:
        """
        Return the list of Tiers tracked in the system.
        """
        # Permissions won't allow this method to be run by non-auth'd users
        objs = Tier.objects.all()
        data = TierSerializer(objs, many=True).data
        return Response(data)
