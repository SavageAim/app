"""
Seed Task; to seed the DB and get the runthrough of the file off of the main thread
"""

# stdlib
from io import StringIO
from os import scandir
from pathlib import Path
# lib
import yaml
from django.conf import settings
from django.core.management import call_command
from django.db import IntegrityError
from django_cloud_tasks.serializers import serialize
from django_cloud_tasks.tasks import SubscriberTask
# local
from .base import SavageAimPublisherTask
from .. import models

TOPIC_NAME = 'seed-db'


class SeedTask(SavageAimPublisherTask):
    @classmethod
    def topic_name(cls) -> str:
        return TOPIC_NAME

    # Define run command that runs the subscriber during eager environments
    def run(
        self,
        message: dict,
        attributes: dict[str, str] | None = None,
        headers: dict[str, str] | None = None,
    ):
        if settings.DJANGO_CLOUD_TASKS_EAGER:
            return SeedTaskSubscriber().run(output=StringIO(), **message)  # fake io for hiding io during tests

        # Real override to fix a bug in the library
        # Cloud PubSub does not support headers, but we simulate them with a key in the data property
        message = self._build_message_with_headers(message=message, headers=headers)
        message['attributes'] = attributes

        return self._get_publisher_client().publish(
            message=serialize(value=message),
            topic_id=self.topic_name(),
            attributes=attributes,
        )


class SeedTaskSubscriber(SubscriberTask):
    @classmethod
    def topic_name(cls) -> str:
        return TOPIC_NAME

    def run(self, output: StringIO | None = None, *args, **kwargs) -> dict:
        print('Beginning Seed of DB', file=output)
        call_command('migrate', stdout=StringIO())
        seed_data_dir = settings.BASE_DIR / 'seed_data'
        gear_data_dir = seed_data_dir / 'gear'

        # Get the Tier and Gear data and import them
        with open(seed_data_dir / 'tiers.yml', 'r') as f:
            print('Seeding Tiers', file=output)
            self.import_file(f, models.Tier, output)

        with scandir(gear_data_dir) as expac_dirs:
            for expac_dir in expac_dirs:
                if not expac_dir.is_dir():
                    continue

                with scandir(expac_dir.path) as gear_files:
                    for file in gear_files:
                        version = Path(file.path).stem
                        print(f'Seeding Gear from {version}', file=output)

                        # Store the version for the file in the DB
                        try:
                            models.XIVVersion.objects.create(version=version)
                        except IntegrityError:
                            pass

                        with open(file.path, 'r') as f:
                            self.import_file(f, models.Gear, output)

        # Lastly we import the Job data.
        # This is handled *slightly* differently because the 'ordering' key in this file will most likely change
        # between expansions, especially for dps
        # So this Integrity Error will be handled slightly differently

        with open(seed_data_dir / 'jobs.yml', 'r') as f:
            print('Seeding Jobs', file=output)
            self.import_jobs(f, output)

        return {'status': 'db_seeded'}

    def import_file(self, file, model, output: StringIO | None):
        data = yaml.safe_load(file)
        for item in data:
            print(f'\t{item["name"]}', file=output)
            _, created = model.objects.get_or_create(**item)
            if not created:
                print('\t\tSkipping, as it is already in the DB.', file=output)

    def import_jobs(self, file, output: StringIO | None):
        """
        Import Job data.
        If Job exists, ensure the ordering value is up to date
        """
        data = yaml.safe_load(file)
        for job in data:
            print(f'\t{job["id"]}', file=output)

            # Check if the Job is already in the Database
            try:
                obj = models.Job.objects.get(pk=job['id'])
                print(
                    f'\t\tAlready exists, ensuring correct ordering ({obj.ordering} -> {job["ordering"]})',
                    file=output,
                )
                obj.ordering = job['ordering']
                obj.save()
            except models.Job.DoesNotExist:
                # If it doesn't exist, just create it!
                models.Job.objects.create(**job)
