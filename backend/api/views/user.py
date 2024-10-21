"""
A view to identify if the user is authenticated or not, for ease
"""

# lib
from drf_spectacular.utils import OpenApiResponse
from drf_spectacular.views import extend_schema
from rest_framework.authtoken.models import Token
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
# local
from .base import APIView
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
    Returns the data of the requesting User.
    If there is no authenticated User, this will return a default set of information, including an `id` of `null`.
    """
    permission_classes = [UserPermissions]
    serializer_class = UserSerializer

    @extend_schema(tags=['user'])
    def get(self, request) -> Response:
        data = UserSerializer(request.user).data
        return Response(data)

    @extend_schema(
        tags=['user'],
        request=SettingsSerializer,
        responses={
            200: OpenApiResponse(description='Settings update was successful!'),
        },
    )
    def put(self, request) -> Response:
        """
        Update the Settings of the logged in User.
        Also allows the User to update their username.
        """
        try:
            obj = request.user.settings
        except Settings.DoesNotExist:
            obj = Settings(user=request.user)

        # Validate the serializer
        serializer = SettingsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        obj.theme = serializer.validated_data.get('theme', obj.theme)
        obj.notifications.update(serializer.validated_data.get('notifications', {}))
        obj.loot_manager_version = serializer.validated_data.get('loot_manager_version', obj.loot_manager_version)
        obj.loot_solver_greed = serializer.validated_data.get('loot_solver_greed', obj.loot_solver_greed)
        obj.save()

        # Update the username
        request.user.first_name = serializer.validated_data.get('username', request.user.first_name)
        request.user.save()

        # Send websocket packet for updates
        self._send_to_user(request.user, {'type': 'settings'})

        return Response(status=200)


class UserTokenView(APIView):
    """
    A view for handling updates to a User's Token.
    """

    @extend_schema(
        tags=['user'],
        request=None,
        responses={
            201: OpenApiResponse(description='API Key regenerated successfully!'),
        },
    )
    def patch(self, request) -> Response:
        """
        Regenerate the User's API Key
        """
        try:
            obj = request.user.auth_token
        except Token.DoesNotExist:
            obj = None

        if obj is not None:
            obj.delete()

        Token.objects.create(user=request.user)

        # Send websocket packet for updates
        self._send_to_user(request.user, {'type': 'settings'})

        return Response(status=201)
