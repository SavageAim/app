"""
Team interaction views

Teams have TeamMember objects that are used to define what characters are involved in them.
This links to requesting users, which is how we check permissions
"""

# lib
from django.core.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
# local
from .base import APIView
from api import notifier
from api.models import Character, Team
from api.serializers import (
    BISListModifySerializer,
    CharacterCollectionSerializer,
)


class TeamProxyCollection(APIView):
    """
    Handle creation of new Proxy Characters for a Team
    """

    def post(self, request: Request, team_id: str) -> Response:
        """
        Create a new Proxy Character in the specified Team.
        Can currently only be done by the Team Lead.
        """
        try:
            obj = Team.objects.filter(
                members__character__user=request.user,
                members__lead=True,
            ).distinct().get(pk=team_id)
        except (Team.DoesNotExist, ValidationError):
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
        obj.members.create(character=char_serializer.instance, bis_list=bis_serializer.instance)

        # Websocket stuff
        self._send_to_team(obj, {'type': 'team', 'id': str(obj.id)})
        for tm in obj.members.all():
            self._send_to_user(tm.character.user, {'type': 'character', 'id': tm.character.pk})

        return Response({'id': char_serializer.instance.pk}, status=201)
