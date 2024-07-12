"""
Simple client that takes an array of item ids and searches the XIVAPI system for them using the ESQL syntax
"""
import os
from typing import Dict
import requests

API_KEY = os.environ.get('XIVAPI_KEY', None)


class XIVAPISearchClient:
    url = 'https://xivapi.com/search'
    indexes = 'item'
    columns = ','.join(['ID', 'Name', 'LevelItem'])

    @classmethod
    def get_item_information(cls, *item_ids: int) -> Dict[str, Dict[str, str]]:
        """
        Given the Item IDs, retrieve their data from XIVAPI and return a map of ids to the name and item_level
        """
        # Compile the payload body and send it to the URL
        payload = {
            'indexes': cls.indexes,
            'columns': cls.columns,
            'body': {
                'query': {
                    'bool': {
                        'filter': [
                            {'ids': {'values': item_ids}}
                        ]
                    }
                }
            }
        }
        url = cls.url
        if API_KEY is not None:
            url += f'?private_key={API_KEY}'
        response = requests.post(url, json=payload)
        response.raise_for_status()

        results = {}
        for item in response.json().get('Results', []):
            results[item['ID']] = {'name': item['Name'], 'item_level': item['LevelItem']}
        
        return results
