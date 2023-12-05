# stdlib
import logging
# lib
import requests
from bs4 import BeautifulSoup


META_JSON_URL = 'https://raw.githubusercontent.com/xivapi/lodestone-css-selectors/main/meta.json'
CHARACTER_JSON_URL = 'https://raw.githubusercontent.com/xivapi/lodestone-css-selectors/main/profile/character.json'
CHARACTER_URL = 'https://eu.finalfantasyxiv.com/lodestone/character/{character_id}'
LOGGER = logging.getLogger(__name__)


class LodestoneScraper:
    """
        Singleton to pull info from the Lodestone.
        Pulls JSON from the lodestone-css-selectors to get the info for the scraper.
    """
    _instance: 'LodestoneScraper' = None
    user_agent: str
    character_json: dict

    def __init__(self) -> None:
        raise NotImplementedError('call .get_instance')

    @classmethod
    def get_instance(cls) -> 'LodestoneScraper':
        if cls._instance:
            return cls._instance

        instance = cls.__new__(cls)

        # Set the fields
        meta_json = requests.get(META_JSON_URL).json()
        instance.user_agent = meta_json['userAgentDesktop']
        instance.character_json = requests.get(CHARACTER_JSON_URL).json()

        cls._instance = instance
        return instance

    def check_token(self, character_id: str, token: str) -> str | None:
        """
            Check the given character for the specified token being present in their bio.
            Return an error string to pass back to the FE if not found, or None if it was.
        """
        url = CHARACTER_URL.format(character_id=character_id)
        response = requests.get(url, headers={'User-Agent': self.user_agent})
        if response.status_code != 200:
            LOGGER.error(f'Received {response.status_code} response from Lodestone.\n\t{response.content}')
            return 'Lodestone may be down.'

        soup = BeautifulSoup(response.content, 'html.parser')

        # Use the Character CSS Selectors to get the element to look at.
        css_class = self.character_json['BIO']['selector']
        for el in soup.select(css_class):
            if token in el.getText():
                return None

        return 'Could not find the verification code in the Lodestone profile.'
