from .test_base import SavageAimTestCase
from ..xivapi_item_search_client import XIVAPISearchClient


class XIVAPISearchTestSuit(SavageAimTestCase):
    """
    Attempt to search the XIVAPI for a set of items, and ensure the correct information is returned.
    """

    def test_search(self):
        """
        Attempt to search the XIVAPI for a set of items, and ensure the correct information is returned.
        """
        expected = {
            42722: {'name': 'Neo Kingdom Thighboots of Fending', 'item_level': 700},
            42788: {'name': 'Skyruin Gunblade', 'item_level': 710},
        }
        self.assertDictEqual(expected, XIVAPISearchClient.get_item_information(*expected.keys()))
