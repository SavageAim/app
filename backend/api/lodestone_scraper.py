# stdlib
import logging
import re
# lib
import requests
from bs4 import BeautifulSoup

META_JSON_URL = 'https://raw.githubusercontent.com/xivapi/lodestone-css-selectors/main/meta.json'
CHARACTER_JSON_URL = 'https://raw.githubusercontent.com/xivapi/lodestone-css-selectors/main/profile/character.json'
CHARACTER_URL = 'https://eu.finalfantasyxiv.com/lodestone/character/{character_id}'
LOGGER = logging.getLogger(__name__)


class CharacterNotFoundError(Exception):
    ...


class LodestoneError(Exception):
    ...


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
            LOGGER.error(f'Received {response.status_code} response from Lodestone for `check_token`.\n\t{response.content}')
            return 'Lodestone may be down.'

        # Use the Character CSS Selectors to get the element to look at.
        soup = BeautifulSoup(response.content, 'html.parser')
        css_class = self.character_json['BIO']['selector']
        el = soup.select_one(css_class)
        if token in el.getText():
            return None

        return 'Could not find the verification code in the Lodestone profile.'
    
    def get_character_data(self, character_id: str) -> dict:
        """
        Given a Character ID, scrape the page for the following information;
            - avatar_url
            - name
            - world
                - Server (DC)
        """
        url = CHARACTER_URL.format(character_id=character_id)
        response = requests.get(url, headers={'User-Agent': self.user_agent})
        if response.status_code == 404:
            # Since this is directly hooked up to an endpoint, we should handle 404s appropriately
            raise CharacterNotFoundError
        elif response.status_code != 200:
            LOGGER.error(f'Received {response.status_code} response from Lodestone for `get_character_data`.\n\t{response.content}')
            raise LodestoneError

        # Use the Character CSS Selectors to get the element to look at.
        soup = BeautifulSoup(response.content, 'html.parser')
        avatar_url = ''
        name = ''
        world = ''
        dc = ''

        # Avatar URL
        selectors = self.character_json['AVATAR']
        css_class = selectors['selector']
        el = soup.select_one(css_class)
        avatar_url = el.get(selectors['attribute']).split('?')[0]

        # Name
        selectors = self.character_json['NAME']
        css_class = selectors['selector']
        el = soup.select_one(css_class)
        name = el.getText()

        # World
        selectors = self.character_json['SERVER']
        css_class = selectors['selector']
        el = soup.select_one(css_class)
        match = re.match(selectors['regex'], el.getText())
        world, dc = match.group('World'), match.group('DC')

        return {
            'avatar_url': avatar_url,
            'name': name,
            'world': world,
            'dc': dc,
        }
