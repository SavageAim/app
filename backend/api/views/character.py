"""
Character interaction views

Characters are tied to requesting users, so implicitly all the views below will follow the same structure
"""

# lib
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

    def get(self, request: Request) -> Response:
        """
        Return a list of Characters belonging to a certain User
        """
        # Permissions won't allow this method to be run by non-auth'd users
        objs = Character.objects.filter(user=request.user)
        data = CharacterCollectionSerializer(objs, many=True).data
        return Response(data)

    def post(self, request: Request) -> Response:
        """
        Characters are verified via celery.
        This view will create the data in the DB
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

    def get(self, request: Request, pk: int) -> Response:
        """
        Read the data of a Character.

        This view will return full data, including a list of gearsets and teams and such
        """
        try:
            obj = Character.objects.get(pk=pk, user=request.user)
        except Character.DoesNotExist:
            return Response(status=404)

        data = CharacterDetailsSerializer(instance=obj).data
        return Response(data)

    def put(self, request: Request, pk: int) -> Response:
        """
        Update certain fields of a Character
        """
        try:
            obj = Character.objects.get(pk=pk, user=request.user, verified=True)
        except Character.DoesNotExist:
            return Response(status=404)

        serializer = CharacterUpdateSerializer(instance=obj, data=request.data)
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


class CharacterVerification(APIView):
    """
    A class specifically for triggering the verification process
    """

    def post(self, request: Request, pk: int) -> Response:
        """
        On receipt of this request, we add the given character to the queue for verification (if needed)
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

    def get(self, request: Request, pk: int) -> Response:
        """
        Check through the DB for any information regarding the Character in question
        """
        try:
            obj = Character.objects.get(pk=pk, user=request.user, verified=True)
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

    def delete(self, request: Request, pk: int) -> Response:
        """
        Delete the Character from the DB, doing all the things that are stated will happen
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
