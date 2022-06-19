from django.core.management.base import BaseCommand
from api.models import TeamMember, TeamMemberPermissions


class Command(BaseCommand):
    help = 'Create initial permissions entries in the DB'

    def handle(self, *args, **options):
        for tm in TeamMember.objects.all():
            try:
                tm.permissions
            except TeamMemberPermissions.DoesNotExist:
                TeamMemberPermissions.objects.create(
                    loot_manager=False,
                    team_characters=False,
                    member=tm,
                )
