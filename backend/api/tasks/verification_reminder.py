from datetime import timedelta
from logging import getLogger

from django.utils import timezone
from django_cloud_tasks.tasks import PeriodicTask

from .. import notifier
from ..models import Character, Notification

logger = getLogger(__name__)


class VerificationReminderTask(PeriodicTask):
    run_every = '@hourly'

    def run(self):
        """
        Find non-verified characters that are 5 days old.
        Send notifications to remind the User to verify
        """
        logger.debug('Running task')
        older_than = timezone.now() - timedelta(days=5)
        logger.debug(f'Reminding unverified characters older than {older_than}.')
        characters = Character.objects.filter(verified=False, user__isnull=False, created__lt=older_than)
        logger.debug(f'Found {characters.count()} characters. Reminding their Users.')
        for char in characters:
            # Check that there wasn't already a reminder sent about this Character
            if not Notification.objects.filter(type='verify_reminder', link=f'/characters/{char.id}/').exists():
                notifier.verify_reminder(char)
