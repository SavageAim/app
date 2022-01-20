from django.core.management.base import BaseCommand
from django.db import IntegrityError, transaction
from api import models


class Command(BaseCommand):
    help = 'Seed the DB with initial data for static models'

    jobs = [
        {'name': 'paladin', 'id': 'PLD', 'display_name': 'Paladin', 'ordering': 0, 'role': 'tank'},
        {'name': 'warrior', 'id': 'WAR', 'display_name': 'Warrior', 'ordering': 1, 'role': 'tank'},
        {'name': 'darkknight', 'id': 'DRK', 'display_name': 'Dark Knight', 'ordering': 2, 'role': 'tank'},
        {'name': 'gunbreaker', 'id': 'GNB', 'display_name': 'Gunbreaker', 'ordering': 3, 'role': 'tank'},

        {'name': 'whitemage', 'id': 'WHM', 'display_name': 'White Mage', 'ordering': 0, 'role': 'heal'},
        {'name': 'scholar', 'id': 'SCH', 'display_name': 'Scholar', 'ordering': 1, 'role': 'heal'},
        {'name': 'astrologian', 'id': 'AST', 'display_name': 'Astrologian', 'ordering': 2, 'role': 'heal'},
        {'name': 'sage', 'id': 'SGE', 'display_name': 'Sage', 'ordering': 3, 'role': 'heal'},

        {'name': 'monk', 'id': 'MNK', 'display_name': 'Monk', 'ordering': 0, 'role': 'dps'},
        {'name': 'dragoon', 'id': 'DRG', 'display_name': 'Dragoon', 'ordering': 1, 'role': 'dps'},
        {'name': 'ninja', 'id': 'NIN', 'display_name': 'Ninja', 'ordering': 2, 'role': 'dps'},
        {'name': 'samurai', 'id': 'SAM', 'display_name': 'Samurai', 'ordering': 3, 'role': 'dps'},
        {'name': 'reaper', 'id': 'RPR', 'display_name': 'Reaper', 'ordering': 4, 'role': 'dps'},

        {'name': 'bard', 'id': 'BRD', 'display_name': 'Bard', 'ordering': 5, 'role': 'dps'},
        {'name': 'machinist', 'id': 'MCH', 'display_name': 'Machinist', 'ordering': 6, 'role': 'dps'},
        {'name': 'dancer', 'id': 'DNC', 'display_name': 'Dancer', 'ordering': 7, 'role': 'dps'},

        {'name': 'blackmage', 'id': 'BLM', 'display_name': 'Black Mage', 'ordering': 8, 'role': 'dps'},
        {'name': 'summoner', 'id': 'SMN', 'display_name': 'Summoner', 'ordering': 9, 'role': 'dps'},
        {'name': 'redmage', 'id': 'RDM', 'display_name': 'Red Mage', 'ordering': 10, 'role': 'dps'},
    ]

    def handle(self, *args, **options):
        # Add the Jobs
        for job_data in self.jobs:
            self.stdout.write(f'Seeding {job_data["id"]}')
            try:
                with transaction.atomic():
                    models.Job.objects.create(**job_data)
            except IntegrityError:
                self.stdout.write('\tSkipping, as it is already in the DB.')
