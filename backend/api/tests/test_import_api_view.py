from io import StringIO

from django.core.management import call_command

from api.models import Gear
from .test_base import SavageAimTestCase
from ..views.base import ImportAPIView


class ImportAPIViewTestSuite(SavageAimTestCase):
    """
    Ensure that gear is correctly imported by the view for finding its IDs
    """

    def setUp(self):
        """
        Call the Gear seed command to prepopulate the DB
        """
        call_command('seed', stdout=StringIO())
        self.selection = Gear.objects.all().values('name', 'id', 'extra_import_classes', 'extra_import_names')

    def test_queensknight_gear(self):
        names_to_check = [
            'Queensknight Falchion',
            'Queensknight Bardiche',
            'Queensknight Faussar',
            'Queensknight Gunblade',
            'Queensknight Spear',
            'Queensknight Scythe',
            'Queensknight Baghnakhs',
            'Queensknight Blade',
            'Queensknight Knives',
            'Queensknight Twinfangs',
            'Queensknight Compound Bow',
            'Queensknight Pistol',
            'Queensknight War Quoits',
            'Queensknight Scepter',
            'Queensknight Foil',
            'Queensknight Flat Brush',
            'Queensknight Cane',
            'Queensknight Astrometer',
            'Queensknight Syrinxi',
            'Book of Chivalry',
            'Word of the Knighthood',
        ]
        expected_id = Gear.objects.get(name='Queensknight').pk
        for name in names_to_check:
            self.assertEqual(ImportAPIView._get_gear_id(self.selection, name), expected_id)
