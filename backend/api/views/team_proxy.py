"""
Team Proxy Management Views

This adjusted views give access to the proxy system and allow users to create and edit proxy characters
"""

# lib
from django.core.exceptions import ValidationError
from drf_spectacular.utils import inline_serializer, OpenApiResponse
from drf_spectacular.views import extend_schema
from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
# local
from .base import APIView
from api.models import Character, Team, TeamMember
from api.serializers import (
    BISListModifySerializer,
    CharacterCollectionSerializer,
    TeamSerializer,
    TeamMemberSerializer,
)

PERMISSION_NAME = 'proxy_manager'


class TeamProxyCollection(APIView):
    """
    Handle creation of new Proxy Characters for a Team
    """

    @extend_schema(
        tags=['team_proxy'],
        request=inline_serializer(
            'TeamProxyMemberCreateRequest',
            {
                'character': CharacterCollectionSerializer,
                'bis_data': BISListModifySerializer,
            },
        ),
        responses={
            201: OpenApiResponse(
                response=inline_serializer('ProxyMemberCreateResponse', {'id': serializers.IntegerField()}),
                description='The ID of the created Proxy Member',
            ),
            400: OpenApiResponse(
                response=inline_serializer(
                    'ProxyMemberCreateValidationErrors',
                    {'character': CharacterCollectionSerializer, 'bis': BISListModifySerializer},
                ),
                description='A map of any errors for the provided Character and BIS data. The values will all be lists of strings for any keys that are present.',
            ),
            404: OpenApiResponse(description='The Team ID does not exist, the Member ID is not valid, or the requesting User does not have permission.'),
        },
    )
    def post(self, request: Request, team_id: str) -> Response:
        """
        Add a new Proxy Member to the Team.
        This request can be run by anyone in the Team with the `proxy_manager` permissions.
        """
        team = self._get_team_with_permission(request, team_id, PERMISSION_NAME)
        if team is None:
            return Response(status=404)

        # Check both serializers against the separate parts of the data
        char_data = request.data.get('character', {})
        bis_data = request.data.get('bis', {})

        char_serializer = CharacterCollectionSerializer(data=char_data)
        char_valid = char_serializer.is_valid()

        bis_serializer = BISListModifySerializer(data=bis_data)
        bis_valid = bis_serializer.is_valid()

        if not (char_valid and bis_valid):
            # One or both are invalid, return errors
            return Response({'character': char_serializer.errors, 'bis': bis_serializer.errors}, status=400)

        # Create objects
        char_serializer.save(user_id=None, token=Character.generate_token())
        bis_serializer.save(name='', owner=char_serializer.instance)

        # Add proxy to team
        team.members.create(character=char_serializer.instance, bis_list=bis_serializer.instance)

        # Websocket stuff
        self._send_to_team(team, {'type': 'team', 'id': str(team.id), 'invite_code': str(team.invite_code)})
        for tm in team.members.all():
            self._send_to_user(tm.character.user, {'type': 'character', 'id': tm.character.pk})

        return Response({'id': char_serializer.instance.pk}, status=201)


class TeamProxyResource(APIView):
    """
    Handle a single Proxy Character record (read / update)
    """

    @extend_schema(
        tags=['team_proxy'],
        responses={
            200: inline_serializer(
                'ProxyMemberReadResponse', 
                {
                    'team': TeamSerializer(),
                    'member': TeamMemberSerializer(),
                },
            ),
            404: OpenApiResponse(description='The Team ID does not exist, the Member ID is not valid, or the requesting User does not have permission.'),
        },
    )
    def get(self, request: Request, team_id: str, pk: int) -> Response:
        """
        Read the details of a specific Proxied Team Member.
        This request can be run by anyone in the Team with the `proxy_manager` permissions.
        """
        team = self._get_team_with_permission(request, team_id, PERMISSION_NAME)
        if team is None:
            return Response(status=404)

        try:
            obj = team.members.filter(character__user__isnull=True).distinct().get(character_id=pk)
        except (TeamMember.DoesNotExist, ValidationError):
            return Response(status=404)

        # Return Team, Character and BIS data separately for ease of use
        team_data = TeamSerializer(instance=team).data
        member_data = TeamMemberSerializer(instance=obj).data
        return Response({'team': team_data, 'member': member_data})

    @extend_schema(
        tags=['team_proxy'],
        request=BISListModifySerializer,
        responses={
            204: OpenApiResponse(
                description='The BIS data of the Proxy Member was updated successfully!',
            ),
            400: OpenApiResponse(
                response=BISListModifySerializer,
                description='A map of any errors for the provided Character and BIS data. The values will all be lists of strings for any keys that are present.',
            ),
            404: OpenApiResponse(description='The Team ID does not exist, the Member ID is not valid, or the requesting User does not have permission.'),
        },
    )
    def put(self, request: Request, team_id: str, pk: int) -> Response:
        """
        Update the BIS information for a Proxy Team Member.
        This request can be run by anyone in the Team with the `proxy_manager` permissions.
        """
        team = self._get_team_with_permission(request, team_id, PERMISSION_NAME)
        if team is None:
            return Response(status=404)

        try:
            obj = team.members.filter(character__user__isnull=True).distinct().get(character_id=pk)
        except (TeamMember.DoesNotExist, ValidationError):
            return Response(status=404)

        # Validate the new BIS List data
        serializer = BISListModifySerializer(instance=obj.bis_list, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(name='')

        # Send a WS updates for BIS and Teams
        self._send_to_user(obj.character.user, {'type': 'bis', 'char': obj.character.id, 'id': serializer.instance.pk})
        for tm in team.members.all():
            self._send_to_team(team, {'type': 'team', 'id': str(team.id), 'invite_code': str(team.invite_code)})

        return Response(status=204)


class TeamProxyClaim(APIView):
    """
    A separate view that handles User attempts to claim a Proxy.
    For a little security, the view will expect the invite code to be sent in the data.
    """

    @extend_schema(
        tags=['team_proxy'],
        request=inline_serializer('ProxyClaimRequest', {'invite_code': serializers.CharField()}),
        responses={
            201: OpenApiResponse(
                response=inline_serializer('ProxyMemberClaimResponse', {'id': serializers.IntegerField()}),
                description='The ID of the copy of the Proxy Member',
            ),
            404: OpenApiResponse(description='The Team ID does not exist, the Member ID is not valid, or the `invite_code` is incorrect.'),
        },
    )
    def post(self, request: Request, team_id: str, pk: int) -> Response:
        """
        Allow a User to make an attempt to claim ownership of a pre-existing Proxy Character.
        This view can be used by anyone who has the `invite_code` for the Team.
        
        It will create a copy of the Character in the requesting User's account.
        When they successfully validate their copy, the system will replace all instances of the proxied Character with their valid one.
        """
        invite_code = request.data.get('invite_code', '')
        try:
            team = Team.objects.get(pk=team_id, invite_code=invite_code)
        except (Team.DoesNotExist, ValidationError):
            return Response(status=404)

        try:
            obj = team.members.filter(character__user__isnull=True).distinct().get(character_id=pk)
        except (TeamMember.DoesNotExist, ValidationError):
            return Response(status=404)

        # Make a copy of the Proxy Character that belongs to the requesting user
        old_char = obj.character
        new_char = Character.objects.create(
            avatar_url=old_char.avatar_url,
            lodestone_id=old_char.lodestone_id,
            name=old_char.name,
            token=Character.generate_token(),
            user=request.user,
            world=old_char.world,
        )

        # Send the new id back to the requesting user
        return Response({'id': new_char.id}, status=201)
