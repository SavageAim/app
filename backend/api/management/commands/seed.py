# lib
from django.core.management.base import BaseCommand
# local
from api.tasks import SeedTask


class Command(BaseCommand):
    help = 'Seed the DB with static data for Gear, Tier and Job information.'

    def handle(self, *args, **options):
        SeedTask.asap()
