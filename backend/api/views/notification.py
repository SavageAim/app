"""
Views to interact with Notification system
"""

# lib
from drf_spectacular.utils import OpenApiResponse
from drf_spectacular.views import extend_schema
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
    queryset = Notification
    serializer_class = NotificationSerializer

    def get(self, request: Request) -> Response:
        """
        Retrieve a list of all the Notifications that were sent to the requesting User.
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
            except ValueError:  # pragma: no cover
                pass

        data = NotificationSerializer(objs, many=True).data
        return Response(data)

    @extend_schema(
        operation_id='notifications_mark_all_as_read',
        request=None,
        responses={
            200: OpenApiResponse(description='All Notifications for the requesting User have been marked as read.'),
        },
    )
    def post(self, request: Request) -> Response:
        """
        Mark all the requesting User's Notifications as read
        """
        Notification.objects.filter(user=request.user).update(read=True)
        return Response()


class NotificationResource(APIView):
    """
    Mark individual notifications as read
    """

    @extend_schema(
        operation_id='notifications_mark_as_read',
        request=None,
        responses={
            200: OpenApiResponse(description='The specified Notification for the requesting User has been marked as read.'),
        },
    )
    def post(self, request: Request, pk: int) -> Response:
        """
        Mark a specific Notification as read for the requesting User.
        If the ID is invalid, for whatever reason, this method will do nothing instead of returning an error.
        """
        Notification.objects.filter(user=request.user, pk=pk).update(read=True)
        return Response()
