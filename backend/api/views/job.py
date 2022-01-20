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
        Return a list of Characters belonging to a certain User
        """
        # Permissions won't allow this method to be run by non-auth'd users
        objs = Job.objects.all()
        data = JobSerializer(objs, many=True).data
        return Response(data)
