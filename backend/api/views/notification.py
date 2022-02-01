"""
Views to interact with Notification system
"""

# lib
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
# local
from api.models import Notification
from api.serializers import (
    NotificationSerializer,
)


class NotificationCollection(APIView):
    """
    Retrieve a list of Notifications
    Send a post request to mark all your notifications as read
    """

    def get(self, request: Request) -> Response:
        """
        List the Notifications
        """
        # Get the filters from the query parameters
        unread = request.query_params.get('unread', False)
        limit = request.query_params.get('limit', None)

        objs = Notification.objects.filter(user=request.user)
        if unread:
            objs = objs.filter(read=False)
        if limit is not None:
            try:
                objs = objs[:int(limit)]
            except ValueError:
                pass

        data = NotificationSerializer(objs, many=True).data
        return Response(data)

    def post(self, request: Request) -> Response:
        """
        Mark all your notifications as read
        """
        Notification.objects.filter(user=request.user).update(read=True)
        return Response()


class NotificationResource(APIView):
    """
    Mark individual notifications as read
    """

    def post(self, request: Request, pk: int) -> Response:
        """
        Mark specific notification as read
        """
        Notification.objects.filter(user=request.user, pk=pk).update(read=True)
        return Response()
