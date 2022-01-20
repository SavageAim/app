"""
Team Member Views

Basically just a management interface of Team Membership;

- Leave / Kick from Team
- Change character / bis list linking
"""

# lib
from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
# local
from api.models import TeamMember
from api.serializers import (
    TeamMemberSerializer,
    TeamMemberModifySerializer,
)


class TeamMemberResource(APIView):
    """
    Management of Team Member Objects
    """

    def get(self, request: Request, team_id: str, pk: id) -> Response:
        """
        Get the Data for a single Team Member record
        """
        try:
            obj = TeamMember.objects.get(pk=pk, team_id=team_id, character__user=request.user)
        except (TeamMember.DoesNotExist, ValidationError):
            return Response(status=404)

        data = TeamMemberSerializer(instance=obj).data
        return Response(data)

    def put(self, request: Request, team_id: str, pk: id) -> Response:
        """
        Update a pre-existing Team Member object, potentially changing both the linked character and bis list
        """
        try:
            obj = TeamMember.objects.get(pk=pk, team_id=team_id, character__user=request.user)
        except (TeamMember.DoesNotExist, ValidationError):
            return Response(status=404)

        serializer = TeamMemberModifySerializer(instance=obj, data=request.data, context={'user': request.user, 'team': obj.team})
        serializer.is_valid(raise_exception=True)

        obj.character_id = serializer.validated_data['character_id']
        obj.bis_list_id = serializer.validated_data['bis_list_id']
        obj.save()

        return Response(status=204)

    # def delete(self, request: Request, team_id: str, pk: id) -> Response:
    #     """
    #     Team Members can leave a team
    #     Team leaders can kick team members
    #     """
    #     try:
    #         obj = TeamMember.objects.get(pk=pk, team_id=team_id)
    #     except (Team.DoesNotExist, ValidationError):
    #         return Response(status=404)

    #     # Check permissions
    #     user_obj = TeamMember.objects.get(team_id=team_id, character__user=request.user)
    #     if user_obj.id != obj.pk and not user_obj.lead:
    #         return Response(status=404)
