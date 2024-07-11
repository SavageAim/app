"""
BIS List interaction views

Can only create and update from these views, no listing since they are returned with a read character
"""
# stdlib
from typing import List
# lib
from django.db.models.deletion import ProtectedError
from rest_framework import serializers
from drf_spectacular.utils import inline_serializer, OpenApiResponse
from drf_spectacular.views import extend_schema
from rest_framework.request import Request
from rest_framework.response import Response
# local
from .base import APIView
from api.models import BISList, Character, Team
from api.serializers import BISListSerializer, BISListModifySerializer


class BISListBaseView(APIView):
    """
    Superclass with the ability to sync BIS Lists and report the sync via websockets
    """

    def _sync_lists(self, list: BISList, sync_ids: List[int]):
        sync_lists = BISList.objects.filter(
            owner=list.owner,
            job=list.job,
            id__in=sync_ids,
        )
        for sync_list in sync_lists:
            sync_list.sync(list)
            self._send_to_user(sync_list.owner.user, {'type': 'bis', 'char': sync_list.owner.id, 'id': sync_list.pk})


class BISListCollection(BISListBaseView):
    """
    Allows for the creation of new BIS Lists
    """
    queryset = BISList
    serializer_class = BISListModifySerializer

    @extend_schema(
        tags=['bis_list'],
        responses={
            201: inline_serializer('CreateResponse', {'id': serializers.IntegerField()}),
            404: OpenApiResponse(description='The given Character ID did not belong to a valid Character owned by the requesting User'),
        },
    )
    def post(self, request: Request, character_id: int) -> Response:
        """
        Create a new BIS List belonging to the specified Character.
        """
        try:
            char = Character.objects.get(pk=character_id, user=request.user)
        except Character.DoesNotExist:
            return Response(status=404)

        # Since we have a valid character, try to create the BISList
        serializer = BISListModifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=char)

        # Send a WS update for BIS
        self._send_to_user(char.user, {'type': 'bis', 'char': char.id, 'id': serializer.instance.pk})

        # Sync lists, if any requested
        self._sync_lists(serializer.instance, request.GET.getlist('sync'))

        # Return the id for redirects
        return Response({'id': serializer.instance.pk}, status=201)


class BISListResource(BISListBaseView):
    """
    Allows for the reading and updating of a BISList
    """

    @extend_schema(
        tags=['bis_list'],
        responses={
            200: BISListSerializer,
            404: OpenApiResponse(
                description=(
                    'The given Character ID did not belong to a valid Character owned by the requesting User.'
                    '\nAlternatively the BISList ID does not belong to a valid Character.'
                )
            ),
        },

    )
    def get(self, request: Request, character_id: int, pk: int) -> Response:
        """
        Read a specific BISList instance, belonging to a specified Character.
        """
        try:
            char = Character.objects.get(pk=character_id, user=request.user)
        except Character.DoesNotExist:
            return Response(status=404)

        try:
            obj = BISList.objects.get(pk=pk, owner=char)
        except BISList.DoesNotExist:
            return Response(status=404)

        data = BISListSerializer(instance=obj).data
        return Response(data)

    @extend_schema(
        tags=['bis_list'],
        request=BISListModifySerializer,
        responses={
            204: OpenApiResponse(description='BISList was updated successfully!'),
            404: OpenApiResponse(
                description=(
                    'The given Character ID did not belong to a valid Character owned by the requesting User.'
                    '\nAlternatively the BISList ID does not belong to a valid Character.'
                )
            ),
        },
    )
    def put(self, request: Request, character_id: int, pk: int) -> Response:
        """
        Update the details of a BISList that belongs to a specified Character.
        """
        try:
            char = Character.objects.get(pk=character_id, user=request.user)
        except Character.DoesNotExist:
            return Response(status=404)

        try:
            obj = BISList.objects.get(pk=pk, owner=char)
        except BISList.DoesNotExist:
            return Response(status=404)

        serializer = BISListModifySerializer(instance=obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Send a WS updates for BIS and Teams
        self._send_to_user(char.user, {'type': 'bis', 'char': char.id, 'id': serializer.instance.pk})
        for tm in obj.teammember_set.all():
            self._send_to_team(
                tm.team,
                {'type': 'team', 'id': str(tm.team.id), 'invite_code': str(tm.team.invite_code)},
            )

        # Sync lists, if any requested
        self._sync_lists(serializer.instance, request.GET.getlist('sync'))

        return Response(status=204)


class BISListDelete(APIView):
    """
    A class specifically for handling the deletion of a BISList.
    Has a GET request to get information on if we can delete this BISList.
    """

    @extend_schema(
        tags=['bis_list'],
        responses={
            200: OpenApiResponse(
                response=inline_serializer(
                    'DeleteReadResponse',
                    {
                        'id': serializers.IntegerField(),
                        'member': serializers.IntegerField(),
                        'name': serializers.CharField(),
                    },
                    many=True,
                ),
                description='A list of places where the BIS List is in use. If this list is empty, the BISList is safe to delete!',
            ),
            404: OpenApiResponse(
                description=(
                    'The given Character ID did not belong to a valid Character owned by the requesting User.'
                    '\nAlternatively the BISList ID does not belong to a valid Character.'
                )
            ),
        },

    )
    def get(self, request: Request, character_id: int, pk: int) -> Response:
        """
        Check if we are able to delete a specified Character's BIS List.

        We can only do this if the BIS List is not in use in any Teams.
        If it is, return names and IDs of the Teams it's in use in so we can provide links in the frontend.
        """
        try:
            char = Character.objects.get(pk=character_id, user=request.user)
        except Character.DoesNotExist:
            return Response(status=404)

        try:
            obj = BISList.objects.get(pk=pk, owner=char)
        except BISList.DoesNotExist:
            return Response(status=404)

        # Information we need to gather;
        #   - Teams the BIS is used in
        teams = Team.objects.filter(members__character=char, members__bis_list=obj)
        info = [{
            'id': team.id,
            'member': team.members.get(character=char, bis_list=obj).pk,
            'name': team.name,
        } for team in teams]

        return Response(info)

    @extend_schema(
        tags=['bis_list'],
        request=BISListModifySerializer,
        responses={
            204: OpenApiResponse(description='BISList was deleted successfully!'),
            400: OpenApiResponse(description='BISList could not be deleted.'),
            404: OpenApiResponse(
                description=(
                    'The given Character ID did not belong to a valid Character owned by the requesting User.'
                    '\nAlternatively the BISList ID does not belong to a valid Character.'
                )
            ),
        },
    )
    def delete(self, request: Request, character_id: int, pk: int) -> Response:
        """
        Delete the BISList from the DB.

        If the BISList is not currently deleteable, this method will return a 400 error.
        """
        try:
            char = Character.objects.get(pk=character_id, user=request.user)
        except Character.DoesNotExist:
            return Response(status=404)

        try:
            obj = BISList.objects.get(pk=pk, owner=char)
        except BISList.DoesNotExist:
            return Response(status=404)

        # Save the id
        bis_id = obj.pk

        # Then delete the object
        try:
            obj.delete()
        except ProtectedError:
            return Response({'message': 'Cannot delete; list is in use.'}, status=400)

        # Send a WS update for BIS
        self._send_to_user(char.user, {'type': 'bis', 'char': char.id, 'id': bis_id})

        return Response(status=204)
