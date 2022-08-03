from django.core.management.base import BaseCommand
from django.db import IntegrityError, transaction
from api import models


class Command(BaseCommand):
    help = 'Seed the DB with initial data for Tiers'

    tiers = [
        # 6.0
        {
            'max_item_level': 605,
            'name': 'Pandæmonium: Asphodelos',
            'raid_gear_name': 'Asphodelos',
            'tome_gear_name': 'Augmented Radiant Host',
        },

        # 6.2
        {
            'max_item_level': 635,
            'name': 'Pandæmonium: Abyssos',
            'raid_gear_name': 'Abyssos',
            'tome_gear_name': 'Augmented Tome',
        },
    ]

    def handle(self, *args, **options):
        # Add the tiers
        for tier_data in self.tiers:
            self.stdout.write(f'Seeding {tier_data["name"]}')
            try:
                with transaction.atomic():
                    models.Tier.objects.create(**tier_data)
            except IntegrityError:
                self.stdout.write('\tSkipping, as it is already in the DB.')
