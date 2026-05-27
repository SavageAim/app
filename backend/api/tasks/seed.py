"""
Seed Task; to seed the DB and get the runthrough of the file off of the main thread
"""

# stdlib
from logging import getLogger
from os import scandir
from pathlib import Path
# lib
import yaml
from django.db import IntegrityError
from django.conf import settings
# local
from .base import SavageAimTask
from .. import models

logger = getLogger(__name__)


class SeedTask(SavageAimTask):
    def run(self):
        logger.info('Beginning Seed of DB')
        seed_data_dir = settings.BASE_DIR / 'seed_data'
        gear_data_dir = seed_data_dir / 'gear'

        # Get the Tier and Gear data and import them
        with open(seed_data_dir / 'tiers.yml', 'r') as f:
            logger.info('Seeding Tiers')
            self.import_file(f, models.Tier)

        with scandir(gear_data_dir) as expac_dirs:
            for expac_dir in expac_dirs:
                if not expac_dir.is_dir():
                    continue

                with scandir(expac_dir.path) as gear_files:
                    for file in gear_files:
                        version = Path(file.path).stem
                        logger.info(f'Seeding Gear from {version}')

                        # Store the version for the file in the DB
                        try:
                            models.XIVVersion.objects.create(version=version)
                        except IntegrityError:
                            pass

                        with open(file.path, 'r') as f:
                            self.import_file(f, models.Gear)

        # Lastly we import the Job data.
        # This is handled *slightly* differently because the 'ordering' key in this file will most likely change
        # between expansions, especially for dps
        # So this Integrity Error will be handled slightly differently

        with open(seed_data_dir / 'jobs.yml', 'r') as f:
            logger.info('Seeding Jobs')
            self.import_jobs(f)

    def import_file(self, file, model):
        data = yaml.safe_load(file)
        for item in data:
            logger.info(f'\t{item["name"]}')
            _, created = model.objects.get_or_create(**item)
            if not created:
                logger.info('\t\tSkipping, as it is already in the DB.')

    def import_jobs(self, file):
        """
        Import Job data.
        If Job exists, ensure the ordering value is up to date
        """
        data = yaml.safe_load(file)
        for job in data:
            logger.info(f'\t{job["id"]}')

            # Check if the Job is already in the Database
            try:
                obj = models.Job.objects.get(pk=job['id'])
                logger.info(
                    f'\t\tAlready exists, ensuring correct ordering ({obj.ordering} -> {job["ordering"]})',
                )
                obj.ordering = job['ordering']
                obj.save()
            except models.Job.DoesNotExist:
                # If it doesn't exist, just create it!
                models.Job.objects.create(**job)
