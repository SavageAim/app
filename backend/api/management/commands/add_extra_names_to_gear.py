from os import scandir
# lib
import yaml
from django.conf import settings
from django.core.management.base import BaseCommand
# local
from api import models


class Command(BaseCommand):
    help = 'Add Extra Names to Gear Objects'

    def handle(self, *args, **options):
        gear_data_dir = settings.BASE_DIR / 'api/management/commands/seed_data/gear'

        # Get Gear data, double check that the Gear has the required information
        with scandir(gear_data_dir) as gear_files:
            for file in gear_files:
                with open(file, 'r') as f:
                    data = yaml.safe_load(f)
                    for item in data:
                        obj = models.Gear.objects.get(name=item['name'], item_level=item['item_level'])
                        changed = False
                        if len(obj.extra_import_names) == 0 and len(item.get('extra_import_names', [])) > 0:
                            changed = True
                            obj.extra_import_names = item['extra_import_names']
                        if len(obj.extra_import_classes) == 0 and len(item.get('extra_import_classes', [])) > 0:
                            changed = True
                            obj.extra_import_classes = item['extra_import_classes']
                        if changed:
                            obj.save()
