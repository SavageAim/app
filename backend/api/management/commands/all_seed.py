from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Run all seed commands in one command, to add it to the docker command'

    def handle(self, *args, **options):
        self.stdout.write('Gear Seed\n')
        call_command('gear_seed', stdout=self.stdout, stderr=self.stderr)
        self.stdout.write('\nJob Seed\n')
        call_command('job_seed', stdout=self.stdout, stderr=self.stderr)
        self.stdout.write('\nTier Seed\n')
        call_command('tier_seed', stdout=self.stdout, stderr=self.stderr)
