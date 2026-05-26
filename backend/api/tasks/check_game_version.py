from django.core.management import call_command
from django_cloud_tasks.tasks import PeriodicTask


class CheckGameVersionTask(PeriodicTask):
    run_every = '0 0 * * *'

    def run(self):
        """
        Check if a new, unseeded, game version has been added to xivapi that we don't have yet
        """
        call_command('check_game_version', '--latest', '--notify')
