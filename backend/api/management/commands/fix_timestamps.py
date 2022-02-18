from datetime import timezone
from django.core.management.base import BaseCommand
from api.models import Character, Notification


class Command(BaseCommand):
    help = 'Fix all the Timestamps in the DB that are missing tzinfo'

    def handle(self, *args, **options):
        for obj in Character.objects.all():
            if obj.created.tzinfo is None:
                self.stdout.write(f'Updating created stamp for {obj}')
                obj.created = obj.created.astimezone(timezone.utc)
                obj.save()

        for obj in Notification.objects.all():
            if obj.timestamp.tzinfo is None:
                self.stdout.write(f'Updating timestamp for {obj}')
                obj.timestamp = obj.timestamp.astimezone(timezone.utc)
                obj.save()
