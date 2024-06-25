# stdlib
from os import scandir
# lib
import yaml
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import IntegrityError, transaction
# local
from api import models


class Command(BaseCommand):
    help = 'Seed the DB with static data for Gear, Tier and Job information.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.HTTP_REDIRECT('Beginning Seed of DB'))
        seed_data_dir = settings.BASE_DIR / 'api/management/commands/seed_data'
        gear_data_dir = seed_data_dir / 'gear'

        # Get the Tier and Gear data and import them
        with open(seed_data_dir / 'tiers.yml', 'r') as f:
            self.stdout.write(self.style.HTTP_REDIRECT('Seeding Tiers'))
            self.import_file(f, models.Tier)

        with scandir(gear_data_dir) as gear_files:
            for file in gear_files:
                self.stdout.write(self.style.HTTP_REDIRECT(f'Seeding Gear from {file.name}'))
                with open(gear_data_dir / file.name, 'r') as f:
                    self.import_file(f, models.Gear)

        # Lastly we import the Job data.
        # This is handled *slightly* differently because the 'ordering' key in this file will most likely change
        # between expansions, especially for dps
        # So this Integrity Error will be handled slightly differently

        with open(seed_data_dir / 'jobs.yml', 'r') as f:
            self.stdout.write(self.style.HTTP_REDIRECT('Seeding Jobs'))
            self.import_jobs(f)

    def import_file(self, file, model):
        data = yaml.safe_load(file)
        for item in data:
            self.stdout.write(f'\t{item["name"]}')
            _, created = model.objects.get_or_create(**item)
            if not created:
                self.stdout.write('\t\tSkipping, as it is already in the DB.')

    def import_jobs(self, file):
        """
        Import Job data.
        If Job exists, ensure the ordering value is up to date
        """
        data = yaml.safe_load(file)
        for job in data:
            self.stdout.write(f'\t{job["id"]}')

            # Check if the Job is already in the Database
            try:
                obj = models.Job.objects.get(pk=job['id'])
                self.stdout.write(
                    f'\t\tAlready exists, ensuring correct ordering ({obj.ordering} -> {job["ordering"]})',
                )
                obj.ordering = job['ordering']
                obj.save()
            except models.Job.DoesNotExist:
                # If it doesn't exist, just create it!
                models.Job.objects.create(**job)
