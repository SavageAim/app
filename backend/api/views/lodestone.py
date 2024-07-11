"""
Webscraping-on-demand endpoint to pull the following info from Lodestone;

{
    avatar_url,
    name,
    world: Server (DC)
}
"""

# lib
from drf_spectacular.utils import inline_serializer, OpenApiResponse
from drf_spectacular.views import extend_schema
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
# local
from api.models import Gear, Job
from api.views.base import ImportAPIView
from ..lodestone_scraper import CharacterNotFoundError, LodestoneError, LodestoneScraper, MismatchedJobError


class LodestoneResource(APIView):
    """
    Retrieve character data for a given Character ID
    """

    @extend_schema(
        responses={
            200: inline_serializer(
                'LodestoneCharacterScrapeResponse',
                {
                    'avatar_url': serializers.URLField(),
                    'name': serializers.CharField(),
                    'world': serializers.CharField(),
                    'dc': serializers.CharField(),
                },
            ),
            400: OpenApiResponse(description='An error occurred when retrieving info from the Lodestone.'),
            404: OpenApiResponse(description='Character ID was not found on the Lodestone.'),
        },
    )
    def get(self, request: Request, character_id: str) -> Response:
        """
        Read the given Character's Lodestone page, and scrape the required information for the system.
        """
        scraper = LodestoneScraper.get_instance()
        try:
            data = scraper.get_character_data(character_id)
        except CharacterNotFoundError:
            return Response({'message': 'Could not find a Character with the given ID.'}, status=404)
        except LodestoneError:
            return Response({'message': 'An error occurred connecting to Lodestone.'}, status=400)

        return Response(data)


class LodestoneGearImport(ImportAPIView):
    """
    Given a Character ID, retrieve its current job and gear details, which the view code can turn into valid gear items
    """

    @extend_schema(
        responses={
            200: inline_serializer(
                'LodestoneGearImportResponse',
                {
                    'mainhand': serializers.IntegerField(),
                    'offhand': serializers.IntegerField(),
                    'head': serializers.IntegerField(),
                    'body': serializers.IntegerField(),
                    'hands': serializers.IntegerField(),
                    'legs': serializers.IntegerField(),
                    'feet': serializers.IntegerField(),
                    'earrings': serializers.IntegerField(),
                    'necklace': serializers.IntegerField(),
                    'bracelet': serializers.IntegerField(),
                    'right_ring': serializers.IntegerField(),
                    'left_ring': serializers.IntegerField(),
                },
            ),
            400: OpenApiResponse(response=inline_serializer('LodestoneImport400Response', {'message': serializers.CharField()})),
            404: OpenApiResponse(response=inline_serializer('LodestoneImport400Response', {'message': serializers.CharField()})),
            406: OpenApiResponse(response=inline_serializer('LodestoneImport400Response', {'message': serializers.CharField()})),
        },
    )
    def get(self, request: Request, character_id: str, expected_job: str) -> Response:
        """
        Read the given Character's Lodestone page, and scrape their currently equipped gear.

        If the gear on the site is not useable by the `expected_job`, this view will return an error.
        """
        try:
            Job.objects.get(id=expected_job)
        except Job.DoesNotExist:
            return Response({'message': f'Invalid job id {expected_job}'}, status=400)

        scraper = LodestoneScraper.get_instance()
        try:
            data = scraper.get_current_gear(character_id, expected_job)
        except CharacterNotFoundError:
            return Response({'message': 'Could not find a Character with the given ID.'}, status=404)
        except LodestoneError:
            return Response({'message': 'An error occurred connecting to Lodestone.'}, status=400)
        except MismatchedJobError as e:
            msg = f'Couldn\'t import Gear from Lodestone. Gear was expected to be for "{expected_job}", but "{e.received}" was found.'
            return Response({'message': msg}, status=406)

        # Now do Levenstein things for matching found gear to Gear objects
        filtered_gear = Gear.objects.filter(
            item_level__gte=data['min_il'],
            item_level__lte=data['max_il'],
        ).values('name', 'id', 'extra_import_classes', 'extra_import_names')
        response = {
            'job_id': expected_job,
            'min_il': data['min_il'],
            'max_il': data['max_il'],
        }
        # Loop through each gear slot and fetch the id based off the name
        for slot, item_name in data['gear'].items():
            if slot in self.ARMOUR_SLOTS:
                response[slot] = self._get_gear_id(filtered_gear.filter(has_armour=True), item_name)
            elif slot in self.ACCESSORY_SLOTS:
                response[slot] = self._get_gear_id(filtered_gear.filter(has_accessories=True), item_name)
            else:
                response[slot] = self._get_gear_id(filtered_gear.filter(has_weapon=True), item_name)

        return Response(response)
