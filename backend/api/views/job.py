"""
Just a view to get the list of all jobs in the system
"""

# lib
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
# local
from api.models import Job
from api.serializers import (
    JobSerializer,
)


class JobCollection(APIView):
    """
    Get a list of Jobs in the system
    """
    queryset = Job
    serializer_class = JobSerializer(many=True)
    permission_classes = [AllowAny]

    def get(self, request: Request) -> Response:
        """
        Return the full list of Jobs in default ordering (Tanks > Healer > Melee > Ranged > Caster)
        """
        # Permissions won't allow this method to be run by non-auth'd users
        objs = Job.objects.all()
        data = JobSerializer(objs, many=True).data
        return Response(data)


class JobSolverSortCollection(APIView):
    """
    Get a list of Jobs in the system, ordered by the default order of how jobs are sorted in the solver by default
    """
    queryset = Job
    serializer_class = JobSerializer(many=True)
    permission_classes = [AllowAny]

    def get(self, request: Request) -> Response:
        """
        Return the full list of Jobs in Loot Solver default order (Melee > Ranged > Caster > Tank > Healer)

        The point of this endpoint is to allow the TeamSettings page to display the ordering of Jobs within the Loot Solver sorting.
        Teams only store overrides, so this view is available to retrieve the default, and then overrides are moved around as needed.
        """
        # Permissions won't allow this method to be run by non-auth'd users
        objs = Job.get_in_solver_order()
        data = JobSerializer(objs, many=True).data
        return Response(data)
