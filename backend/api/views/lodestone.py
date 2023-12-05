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
from ..lodestone_scraper import CharacterNotFoundError, LodestoneError, LodestoneScraper


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
