# lib
import yaml
from django.conf import settings
from django.core.management.base import BaseCommand
# local
from api import models


class Command(BaseCommand):
    help = 'Add fights to existing Tiers (EW only)'

    def handle(self, *args, **options):
        seed_data_dir = settings.BASE_DIR / 'api/management/commands/seed_data'

        # Get the Tier and Gear data and import them
        with open(seed_data_dir / 'tiers.yml', 'r') as f:
            data = yaml.safe_load(f)
            for item in data:
                obj = models.Tier.objects.get(name=item['name'])
                if len(obj.fights) == 0:
                    obj.fights = item['fights']
                    obj.save()
