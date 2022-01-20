"""
A view to identify if the user is authenticated or not, for ease
"""

# lib
from rest_framework.views import APIView
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
# local
from api.models import Settings
from api.serializers import SettingsSerializer, UserSerializer


class UserPermissions(BasePermission):
    """
    Allow any to GET, only authenticated for PUT
    """

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return request.user.is_authenticated


class UserView(APIView):
    """
    A simple method to get the (useful) information about the current user.
    Will return 404 if the request is unauthenticated, which will prompt the UI to display a login button instead
    """
    permission_classes = [UserPermissions]

    def get(self, request) -> Response:
        data = UserSerializer(request.user).data
        return Response(data)

    def put(self, request) -> Response:
        """
        Update a User's serializer
        """
        try:
            obj = request.user.settings
        except Settings.DoesNotExist:
            obj = Settings(user=request.user)

        # Validate the serializer
        serializer = SettingsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        obj.theme = serializer.validated_data['theme']
        obj.save()
        return Response(status=201)
