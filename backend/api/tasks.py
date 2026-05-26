"""
Set up our tasks for celery to run

Task to verify accounts on XIVAPI.
"""
# stdlib
from datetime import timedelta
# lib
from asgiref.sync import async_to_sync
from celery import shared_task
from celery.utils.log import get_task_logger
from channels.layers import get_channel_layer
from django.core.management import call_command
from django.db.models import Q
from django.utils import timezone
# local
from . import notifier
from .lodestone_scraper import LodestoneScraper
from .models import Character, Notification, Team

logger = get_task_logger(__name__)


@shared_task(name='verify_reminder')
def remind_users_to_verify():
    """
    Find non-verified Characters that are 5 days old.
    Send Notifications to remind the User to verify.
    """
    logger.debug(f'Running at: {timezone.now()}')
    older_than = timezone.now() - timedelta(days=5)
    logger.debug(f'Reminding unverified characters older than {older_than}.')

    characters = Character.objects.filter(verified=False, user__isnull=False, created__lt=older_than)
    logger.debug(f'Found {characters.count()} characters. Reminding their Users.')
    for char in characters:
        # Check that there wasn't already a reminder sent about this Character
        if not Notification.objects.filter(type='verify_reminder', link=f'/characters/{char.id}/').exists():
            notifier.verify_reminder(char)


@shared_task(name='cleanup')
def cleanup():
    """
    Cleanup the DB of all unverified (non-proxy) characters made more than 7 days ago
    """
    logger.debug(f'Running at: {timezone.now()}')
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


@shared_task(name='refresh_tokens')
def refresh_tokens():
    """
    Refresh any tokens that are about to expire
    """
    call_command('refresh_tokens')


@shared_task(name='check_game_version')
def check_game_version():
    """
    Check if a new, unseeded, game version has been added to xivapi that we don't have yet
    """
    call_command('check_game_version', '--latest', '--notify')
