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


def assimilate_proxies(real_char: Character):
    # Find all Proxy characters that have the same lodestone ID as this one
    proxies = Character.objects.filter(
        Q(user__isnull=True) | Q(user_id=real_char.user_id),
        lodestone_id=real_char.lodestone_id,
    )

    # For each Character (which should only ever be in one team each);
    #   - Notify the Team Leader that the claim has happened
    #   - Move the BIS List to the real Character, name it using the Team's name
    #   - Update the TeamMember object to point to this character
    for char in proxies:
        for tm in char.teammember_set.all():
            if char.user is None:
                notifier.team_proxy_claim(tm)

            bis = tm.bis_list
            bis.owner = real_char
            bis.name = f'BIS From {tm.team.name}'
            bis.save()

            tm.character = real_char
            tm.save()


@shared_task(name='verify_character')
def verify_character(pk: int):
    """
    Verify the character has the expected token in the bio on xivapi.

    If so, update the flag to True, and delete all other unverified characters with the same lodestone id
    """
    # Check that the character is unverified and exists
    logger.info(f'Commencing verification attempt for Character #{pk}.')
    try:
        obj = Character.objects.get(pk=pk, verified=False)
    except Character.DoesNotExist:
        logger.warn(f'Character #{pk} either does not exist or is verified. Exiting.')
        return

    # Call the xivapi function in a sync context
    logger.debug('calling lookup function')
    err = LodestoneScraper.get_instance().check_token(obj.lodestone_id, obj.token)
    logger.debug('finished lookup function')

    if err is not None:
        notifier.verify_fail(obj, err)
        logger.info(f'Character #{pk} could not be verified. Exiting. ({err})')
        return

    logger.info(f'Character #{pk} verified. Updating DB.')
    # First we update the flag on the object specified
    obj.verified = True
    obj.save()

    # Before we go deleting any Characters, we need to sort all the Proxies that share the lodestone ID
    assimilate_proxies(obj)

    # Next delete all unverified instances of the character (this includes proxies)
    logger.info(f'Deleting unverified instances of Character #{obj.lodestone_id} (#{pk}) owned by {obj.user_id}.')
    objs = Character.objects.filter(
        Q(user__isnull=True) | Q(user_id=obj.user_id),
        verified=False,
        lodestone_id=obj.lodestone_id,
    ).exclude(pk=pk)
    ids_to_delete = [o.pk for o in objs]
    logger.info(f'Found {objs.count()} instances of Character #{obj.lodestone_id} to delete.\n{ids_to_delete}')
    objs.delete()
    # Then we're done!
    notifier.verify_success(obj)
    # Also send websocket details
    channel_layer = get_channel_layer()
    if channel_layer is not None:
        async_to_sync(channel_layer.group_send)(f'user-updates-{obj.user.id}', {'type': 'character', 'id': obj.pk})


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
