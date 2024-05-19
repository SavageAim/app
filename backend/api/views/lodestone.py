"""
Webscraping-on-demand endpoint to pull the following info from Lodestone;

{
    avatar_url,
    name,
    world: Server (DC)
}
"""

# lib
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

    def get(self, request: Request, character_id: str) -> Response:
        """
        Scrape the Lodestone and return the found character data
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

    def get(self, request: Request, character_id: str, expected_job: str) -> Response:
        """
        Scrape the Lodestone and return the gear and job information
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
            msg = f'Error occurred when attempting to import gear. Gear was expected to be for "{expected_job}", but "{e.received}" was found.'
            return Response({'message': msg}, status=406)

        # Now do Levenstein things for matching found gear to Gear objects
        filtered_gear = Gear.objects.filter(
            item_level__gte=data['min_il'],
            item_level__lte=data['max_il'],
        ).values('name', 'id')
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
