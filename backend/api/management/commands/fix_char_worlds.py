from django.core.management.base import BaseCommand
from api.models import Character
from api.serializers.character import NEW_WORLD_PATTERN


class Command(BaseCommand):
    help = 'Fix any characters that have been imported while the world names are broken'

    def handle(self, *args, **options):
        for obj in Character.objects.all():
            find = NEW_WORLD_PATTERN.findall(obj.world)
            if len(find) == 1:
                self.stdout.write(f'Found bad world pattern - {obj.world}')
                world = f'{find[0][0]} ({find[0][1]})'
                self.stdout.write(f'Replaced with - {world}')
                obj.world = world
                obj.save()
