"""
Character interaction views

Characters are tied to requesting users, so implicitly all the views below will follow the same structure
"""

# lib
from drf_spectacular.utils import inline_serializer, OpenApiResponse
from drf_spectacular.views import extend_schema
from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
# local
from .base import APIView
from api.models import Character, Team
from api.serializers import (
    CharacterCollectionSerializer,
    CharacterDetailsSerializer,
    CharacterUpdateSerializer,
)
from api.tasks import verify_character


class CharacterCollection(APIView):
    """
    Methods to interact with a list of Characters belonging to a User.
    Provides list and create methods.
    """

    @extend_schema(
        responses={
            200: OpenApiResponse(
                response=CharacterCollectionSerializer(many=True),
                description='List of all the Characters belonging to the User.',
            ),
        },
        operation_id='character_list',
    )
    def get(self, request: Request) -> Response:
        """
        Retrieve all of the Characters belonging to the requesting User.
        """
        # Permissions won't allow this method to be run by non-auth'd users
        objs = Character.objects.filter(user=request.user)
        data = CharacterCollectionSerializer(objs, many=True).data
        return Response(data)

    @extend_schema(
        request=CharacterCollectionSerializer,
        responses={
            201: OpenApiResponse(
                response=inline_serializer('CreateResponse', {'id': serializers.IntegerField()}),
                description='The ID of the created Character',
            ),
        },
        operation_id='character_create',
    )
    def post(self, request: Request) -> Response:
        """
        Create a new, un-verified Character, that belongs to the requesting User.
        """
        # Put the sent data into the serializer for validation
        serializer = CharacterCollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, token=Character.generate_token())

        # Send WS update
        self._send_to_user(request.user, {'type': 'character', 'id': serializer.instance.pk})

        # Return the id for redirects
        return Response({'id': serializer.instance.pk}, status=201)


class CharacterResource(APIView):
    """
    Handling character specific requests
    """

    @extend_schema(
        responses={
            200: CharacterDetailsSerializer,
            404: OpenApiResponse(
                description='The given Character ID did not belong to a valid Character owned by the requesting User.',
            ),
        },
        operation_id='character_read',
    )
    def get(self, request: Request, pk: int) -> Response:
        """
        Read the data of a specified Character.

        This endpoint will return the full data of the Character, including associated BISLists and Teams.
        """
        try:
            obj = Character.objects.get(pk=pk, user=request.user)
        except Character.DoesNotExist:
            return Response(status=404)

        data = CharacterDetailsSerializer(instance=obj).data
        return Response(data)

    @extend_schema(
        request=CharacterUpdateSerializer,
        responses={
            204: OpenApiResponse(description='Character was successfully updated!'),
            404: OpenApiResponse(
                description='The given Character ID did not belong to a valid Character owned by the requesting User.',
            ),
        },
        operation_id='character_update',
    )
    def put(self, request: Request, pk: int, partial: bool = False) -> Response:
        """
        Update the information of a Character.

        Requires sending the full object to update.
        """
        try:
            obj = Character.objects.get(pk=pk, user=request.user)
        except Character.DoesNotExist:
            return Response(status=404)

        serializer = CharacterUpdateSerializer(instance=obj, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Send WS updates
        self._send_to_user(request.user, {'type': 'character', 'id': obj.id})
        for tm in obj.teammember_set.all():
            self._send_to_team(
                tm.team,
                {'type': 'team', 'id': str(tm.team.id), 'invite_code': str(tm.team.invite_code)},
            )

        return Response(status=204)

    @extend_schema(
        request=CharacterUpdateSerializer,
        responses={
            204: OpenApiResponse(description='Character was successfully updated!'),
            404: OpenApiResponse(
                description='The given Character ID did not belong to a valid Character owned by the requesting User.',
            ),
        },
        operation_id='character_partial_update',
    )
    def patch(self, request: Request, pk: int) -> Response:
        """
        Update the information of a Character.

        Can handle partial update requests, only changed fields need to be sent to this endpoint.
        """
        return self.put(request, pk, True)


class CharacterVerification(APIView):
    """
    A class specifically for triggering the verification process
    """

    @extend_schema(
        request=CharacterUpdateSerializer,
        responses={
            202: OpenApiResponse(description='Character verification has been requested!'),
            404: OpenApiResponse(
                description='The given Character ID did not belong to a valid, unverified, Character owned by the requesting User.',
            ),
        },
        operation_id='request_character_verification',
    )
    def post(self, request: Request, pk: int) -> Response:
        """
        Trigger the verification process for a given Character.

        The process involves checking that the token associated with the Character is present on the Lodestone profile.
        """
        try:
            Character.objects.get(pk=pk, user=request.user, verified=False)
        except Character.DoesNotExist:
            return Response(status=404)

        # Do some celery stuff!
        verify_character.delay(pk)

        return Response(status=202)


class CharacterDelete(APIView):
    """
    A class specifically for handling the deletion of a Character.
    Has a GET request to get what will be affected by the deletion of this Character.
    """

    @extend_schema(
        responses={
            200: OpenApiResponse(
                response=inline_serializer(
                    'CharacterDeleteReadResponse',
                    {
                        'lead': serializers.BooleanField(),
                        'members': serializers.IntegerField(),
                        'name': serializers.CharField(),
                    },
                    many=True,
                ),
                description='A list of Teams that will be affected by the Character\'s deletion.',
            ),
            404: OpenApiResponse(
                description='The given Character ID did not belong to a valid Character owned by the requesting User.',
            ),
        },
        operation_id='character_delete_check',
    )
    def get(self, request: Request, pk: int) -> Response:
        """
        Check what will happen if this Character would be deleted.
        Returns a list of Teams that the Character is in, including the following fields;
        - name: The name of the Team
        - lead: Whether the Character is the leader of the Team.
        - members: How many members are in the Team.
        """
        try:
            obj = Character.objects.get(pk=pk, user=request.user)
        except Character.DoesNotExist:
            return Response(status=404)

        # Information we need to gather;
        #   - Teams the character is in, and whether they lead it or not
        teams = Team.objects.filter(members__character=obj)
        info = [{
            'name': team.name,
            'lead': team.members.get(character=obj).lead,
            'members': team.members.count(),
        } for team in teams]

        return Response(info)

    @extend_schema(
        responses={
            204: OpenApiResponse(description='Character was deleted successfully!'),
            404: OpenApiResponse(
                description='The given Character ID did not belong to a valid Character owned by the requesting User.',
            ),
        },
        operation_id='character_delete',
    )
    def delete(self, request: Request, pk: int) -> Response:
        """
        Delete the Character from the system.
        This can also trigger the following effects where appropriate;
        - Disbanding Teams where the Character is the only Member
        - Handing leadership of a Team to another Member if the Character is the leader
        - Leaving the Team if the Character is not the leader.
        """
        try:
            obj = Character.objects.get(pk=pk, user=request.user)
        except Character.DoesNotExist:
            return Response(status=404)

        # Save data for the WS update
        char_id = obj.pk
        teams = obj.teammember_set.all()

        # Call character.remove to cleanup teams first
        obj.remove()

        # Then delete the object
        obj.delete()

        # Send WS updates
        self._send_to_user(request.user, {'type': 'character', 'id': char_id})
        for tm in teams:
            self._send_to_team(
                tm.team,
                {'type': 'team', 'id': str(tm.team.id), 'invite_code': str(tm.team.invite_code)},
            )
            # Potential need to clean up here, but I don't feel like it's too big of an issue

        return Response(status=204)
