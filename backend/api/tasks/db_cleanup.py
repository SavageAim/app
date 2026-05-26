from datetime import timedelta
from logging import getLogger

from django.utils import timezone
from django_cloud_tasks.tasks import PeriodicTask

from ..models import Character, Team

logger = getLogger(__name__)


class DBCleanupTask(PeriodicTask):
    run_every = '0 * * * *'

    def run(self):
        """
        Cleanup the DB of all unverified (non-proxy) characters made more than 7 days ago
        """
        logger.debug('Running task')
        older_than = timezone.now() - timedelta(days=7)
        logger.debug(f'Deleting unverified characters older than {older_than}.')

        objs = Character.objects.filter(verified=False, user__isnull=False, created__lt=older_than)
        logger.debug(f'Found {objs.count()} characters. Deleting them.')
        for char in objs:
            # Remove them from every team they are a member of
            teams = Team.objects.filter(members__character=char).distinct()
            for team in teams:
                team.remove_character(char, False)

            char.bis_lists.all().delete()
            char.delete()
