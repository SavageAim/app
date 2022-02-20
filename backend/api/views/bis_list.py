"""
BIS List interaction views

Can only create and update from these views, no listing since they are returned with a read character
"""
# lib
from django.db.models.deletion import ProtectedError
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
# local
from api.models import BISList, Character, Team
from api.serializers import BISListSerializer, BISListModifySerializer


class BISListCollection(APIView):
    """
    Allows for the creation of new BIS Lists
    """

    def post(self, request: Request, character_id: int) -> Response:
        """
        Create a BIS List belonging to the specified character
        """
        try:
            char = Character.objects.get(pk=character_id, user=request.user, verified=True)
        except Character.DoesNotExist:
            return Response(status=404)

        # Since we have a valid character, try to create the BISList
        serializer = BISListModifySerializer(data=request.data, context={'owner': char})
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=char)

        # Return the id for redirects
        return Response({'id': serializer.instance.pk}, status=201)


class BISListResource(APIView):
    """
    Allows for the reading and updating of a BISList
    """

    def get(self, request: Request, character_id: int, pk: int) -> Response:
        """
        Read a BISList
        """
        try:
            char = Character.objects.get(pk=character_id, user=request.user, verified=True)
        except Character.DoesNotExist:
            return Response(status=404)

        try:
            obj = BISList.objects.get(pk=pk, owner=char)
        except BISList.DoesNotExist:
            return Response(status=404)

        data = BISListSerializer(instance=obj).data
        return Response(data)

    def put(self, request: Request, character_id: int, pk: int) -> Response:
        """
        Update an existing BISList
        """
        try:
            char = Character.objects.get(pk=character_id, user=request.user, verified=True)
        except Character.DoesNotExist:
            return Response(status=404)

        try:
            obj = BISList.objects.get(pk=pk, owner=char)
        except BISList.DoesNotExist:
            return Response(status=404)

        serializer = BISListModifySerializer(instance=obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=204)


class BISListDelete(APIView):
    """
    A class specifically for handling the deletion of a BISList.
    Has a GET request to get information on if we can delete this BISList.
    """

    def get(self, request: Request, character_id: int, pk: int) -> Response:
        """
        Check if we are able to delete a sepcified BIS List.

        We can only do this if the BIS List is not in use in any Teams.
        If it is, return names and IDs of the Teams it's in use in so we can provide links in the frontend.
        """
        try:
            char = Character.objects.get(pk=character_id, user=request.user, verified=True)
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
            'name': team.name,
        } for team in teams]

        return Response(info)

    def delete(self, request: Request, character_id: int, pk: int) -> Response:
        """
        Delete the BISList from the DB, ensuring that we can.
        """
        try:
            char = Character.objects.get(pk=character_id, user=request.user, verified=True)
        except Character.DoesNotExist:
            return Response(status=404)

        try:
            obj = BISList.objects.get(pk=pk, owner=char)
        except BISList.DoesNotExist:
            return Response(status=404)

        # Then delete the object
        try:
            obj.delete()
        except ProtectedError:
            return Response({'message': 'Cannot delete; list is in use.'}, status=400)
        return Response(status=204)
