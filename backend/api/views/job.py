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

    permission_classes = [AllowAny]

    def get(self, request: Request) -> Response:
        """
        Return the full list of Jobs in default ordering (Melee > Ranged > Caster > Tanks > Healer)
        """
        # Permissions won't allow this method to be run by non-auth'd users
        objs = Job.get_in_solver_order()
        data = JobSerializer(objs, many=True).data
        return Response(data)
