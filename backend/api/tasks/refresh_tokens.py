from django.core.management import call_command
from django_cloud_tasks.tasks import PeriodicTask


class RefreshTokensTask(PeriodicTask):
    run_every = '@daily'

    def run(self):
        """
        Refresh any tokens that are about to expire
        """
        call_command('refresh_tokens')
