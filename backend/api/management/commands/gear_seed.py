from django.core.management.base import BaseCommand
from django.db import IntegrityError, transaction
from api import models


class Command(BaseCommand):
    help = 'Seed the DB with initial data for gear'

    gear = [
        # 6.0
        {'has_accessories': True, 'has_armour': False, 'has_weapon': False, 'item_level': 560, 'name': 'The Last'},
        {'has_accessories': False, 'has_armour': True, 'has_weapon': True, 'item_level': 560, 'name': 'Endwalker AF'},
        {'has_accessories': True, 'has_armour': True, 'has_weapon': True, 'item_level': 570, 'name': 'Moonward'},
        {'has_accessories': True, 'has_armour': False, 'has_weapon': False, 'item_level': 580, 'name': 'Eternal Dark'},
        {'has_accessories': False, 'has_armour': False, 'has_weapon': True, 'item_level': 580, 'name': 'Divine Light'},

        # 6.0.1
        {'has_accessories': True, 'has_armour': True, 'has_weapon': False, 'item_level': 580, 'name': 'Limbo'},

        # 6.0.5
        {'has_accessories': True, 'has_armour': True, 'has_weapon': True, 'item_level': 580, 'name': 'Classical'},
        {'has_accessories': True, 'has_armour': True, 'has_weapon': True, 'item_level': 590, 'name': 'Radiant Host'},
        {'has_accessories': True, 'has_armour': True, 'has_weapon': True, 'item_level': 600, 'name': 'Augmented Radiant Host'},
        {'has_accessories': True, 'has_armour': True, 'has_weapon': False, 'item_level': 600, 'name': 'Asphodelos'},
        {'has_accessories': False, 'has_armour': False, 'has_weapon': True, 'item_level': 605, 'name': 'Asphodelos'},
    ]

    def handle(self, *args, **options):
        # Add the gear
        for gear_data in self.gear:
            self.stdout.write(f'Seeding {gear_data["name"]}')
            try:
                with transaction.atomic():
                    models.Gear.objects.create(**gear_data)
            except IntegrityError:
                self.stdout.write('\tSkipping, as it is already in the DB.')
