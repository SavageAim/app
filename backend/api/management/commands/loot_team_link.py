from django.core.management.base import BaseCommand
from api.models import Loot


class Command(BaseCommand):
    help = 'Fix the Team FK in Loot model'

    def handle(self, *args, **options):
        for obj in Loot.objects.all():
            if obj.member is not None:
                self.stdout.write(f'Adding team link to {obj}')
                obj.team = obj.member.team
                obj.save()
