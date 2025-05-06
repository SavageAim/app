from django.core.management.base import BaseCommand
from api.models import BISList


class Command(BaseCommand):
    help = 'Call .save() on all BISLists to handle the ring swapping.'

    def handle(self, *args, **options):
        for obj in BISList.objects.all():
            obj.save()
