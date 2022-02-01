from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from api import models


class Command(BaseCommand):
    help = 'Set / Update the initial values of the notification details for every user.'

    def handle(self, *args, **options):
        # Add the tiers
        for user in User.objects.all():
            try:
                for key in models.Settings.NOTIFICATIONS:
                    if key not in user.settings.notifications:
                        user.settings.notifications[key] = True
                user.settings.save()
            except models.Settings.DoesNotExist:
                models.Settings.objects.create(
                    user=user,
                    theme='beta',
                    notifications={key: True for key in models.Settings.NOTIFICATIONS},
                )
