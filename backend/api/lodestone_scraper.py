# stdlib
import logging
import re
from typing import Optional
# lib
import requests
from bs4 import BeautifulSoup

META_JSON_URL = 'https://raw.githubusercontent.com/xivapi/lodestone-css-selectors/main/meta.json'
CHARACTER_JSON_URL = 'https://raw.githubusercontent.com/xivapi/lodestone-css-selectors/main/profile/character.json'
GEARSET_JSON_URL = 'https://raw.githubusercontent.com/freyamade/lodestone-css-selectors/main/profile/gearset.json'
CHARACTER_URL = 'https://eu.finalfantasyxiv.com/lodestone/character/{character_id}'
LOGGER = logging.getLogger(__name__)

# Create some sets of things for the current gear import
SPECIAL_ALLOWED_CLASSLISTS = {
    'Disciples of War or Magic',
    'All Classes',
}
IGNORED_SLOTS = {
    'WAIST',
    'SOULCRYSTAL',
}
# Also set up a mapping of SLOT_NAME to slotname
LODESTONE_TO_SA_NAME_MAP = {
    'MAINHAND': 'mainhand',
    'OFFHAND': 'offhand',
    'HEAD': 'head',
    'BODY': 'body',
    'HANDS': 'hands',
    'LEGS': 'legs',
    'FEET': 'feet',
    'EARRINGS': 'earrings',
    'NECKLACE': 'necklace',
    'BRACELETS': 'bracelet',
    'RING1': 'right_ring',
    'RING2': 'left_ring',
}


class CharacterNotFoundError(Exception):
    ...


class LodestoneError(Exception):
    ...


class MismatchedJobError(Exception):
    received: str

    def __init__(self, received: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.received = received


class LodestoneScraper:
    """
    Singleton to pull info from the Lodestone.
    Pulls JSON from the lodestone-css-selectors to get the info for the scraper.
    """
    _instance: 'LodestoneScraper' = None
    user_agent: str
    character_json: dict
    gearset_json: dict

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
        instance.gearset_json = requests.get(GEARSET_JSON_URL).json()

        cls._instance = instance
        return instance

    def check_token(self, character_id: str, token: str) -> Optional[str]:
        """
        Check the given character for the specified token being present in their bio.
        Return an error string to pass back to the FE if not found, or None if it was.
        """
        url = CHARACTER_URL.format(character_id=character_id)
        response = requests.get(url, headers={'User-Agent': self.user_agent})
        if response.status_code != 200:
            LOGGER.error(
                f'Received {response.status_code} response from Lodestone for `check_token`.'
                f'\n\t{response.content}',
            )
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
            LOGGER.error(
                f'Received {response.status_code} response from Lodestone for `get_character_data`.'
                f'\n\t{response.content}',
            )
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

    def get_current_gear(self, character_id: str, expected_job: str):
        """
        Fetch and parse the the character's page to retrieve the current gear.
        The gear must be equippable by the given job.
        """
        url = CHARACTER_URL.format(character_id=character_id)
        response = requests.get(url, headers={'User-Agent': self.user_agent})
        if response.status_code == 404:
            # Since this is directly hooked up to an endpoint, we should handle 404s appropriately
            raise CharacterNotFoundError
        elif response.status_code != 200:
            LOGGER.error(
                f'Received {response.status_code} response from Lodestone for `get_character_data`.'
                f'\n\t{response.content}',
            )
            raise LodestoneError

        # Parse each of the slots from the website, and turn them into our local copies of gear
        soup = BeautifulSoup(response.content, 'html.parser')
        max_il = float('-inf')
        min_il = float('inf')

        slot_map = {}
        for slot_name, selectors in self.gearset_json.items():
            if (slot_name == 'OFFHAND' and expected_job != 'PLD') or slot_name in IGNORED_SLOTS:
                continue

            class_list = soup.select_one(selectors['CLASS_LIST']['selector']).getText()
            if expected_job not in class_list and class_list not in SPECIAL_ALLOWED_CLASSLISTS:
                raise MismatchedJobError(class_list)

            gear_name = soup.select_one(selectors['NAME']['selector']).getText()
            item_level = int(soup.select_one(selectors['ITEM_LEVEL']['selector']).getText().split(' ')[-1])

            if item_level > max_il:
                max_il = item_level
            if item_level < min_il:
                min_il = item_level

            slot_map[LODESTONE_TO_SA_NAME_MAP[slot_name]] = gear_name

        # Handling for non-PLDs
        if expected_job != 'PLD':
            slot_map['offhand'] = slot_map['mainhand']

        return {
            'gear': slot_map,
            'max_il': max_il,
            'min_il': min_il,
        }
