"""
Simple client that takes an array of item ids and searches the XIVAPI system for them using the ESQL syntax
"""
import os
from typing import Dict
import requests

API_KEY = os.environ.get('XIVAPI_KEY', None)


class XIVAPISearchClient:
    url = 'https://beta.xivapi.com/api/1/sheet/Item'

    @classmethod
    def get_item_information(cls, *item_ids: int) -> Dict[str, Dict[str, str]]:
        """
        Given the Item IDs, retrieve their data from XIVAPI and return a map of ids to the name and item_level
        """
        results = {}
        item_ids = set(item_ids)
        rows = ','.join(str(item_id) for item_id in item_ids)
        url = f'{cls.url}?rows={rows}&fields=row_id,LevelItem.value,Name'
        response = requests.get(url)
        response.raise_for_status()

        for item in response.json().get('rows', []):
            results[item['row_id']] = {'name': item['fields']['Name'], 'item_level': item['fields']['LevelItem']['value']}

        if len(results) != len(item_ids):
            raise ValueError(f'Expected {len(item_ids)} items, retrieved {len(results)}')

        return results
