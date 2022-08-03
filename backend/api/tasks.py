"""
Set up our tasks for celery to run

Task to verify accounts on XIVAPI.
"""
# stdlib
from datetime import timedelta
from typing import Optional
# lib
import requests
from asgiref.sync import async_to_sync
from bs4 import BeautifulSoup
from celery import shared_task
from celery.utils.log import get_task_logger
from channels.layers import get_channel_layer
from django.utils import timezone
# local
from . import notifier
from .models import Character

logger = get_task_logger(__name__)
USER_AGENT = (
    'Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/46.0.2490.76 Mobile Safari/537.36'
)


def xivapi_lookup(pk: str, token: str, log) -> Optional[str]:
    """
    Actually check XIVAPI for the specified token being present in the specified character's bio
    """
    # We're gonna have to scrape the webpage similar to how FFXIVCollect does it
    url = f'https://eu.finalfantasyxiv.com/lodestone/character/{pk}'
    response = requests.get(url, headers={'User-Agent': USER_AGENT})
    if response.status_code != 200:
        log.error(f'Received {response.status_code} response from Lodestone. Cannot verify right now.')
        return 'Lodestone may be down.'

    soup = BeautifulSoup(response.content, 'html.parser')

    # Find a div with either character__selfintroduction or character__character_profile
    # Get the text in them, check if the text contains the token we're looking for

    # Attempt the selfintroduction one first
    for el in soup.find_all('div', class_='character__selfintroduction'):
        if token in el.getText():
            return None

    for el in soup.find_all('div', class_='character__character_profile'):
        if token in el.getText():
            return None

    return 'Could not find the verification code in the Lodestone profile.'


def assimilate_proxies(real_char: Character):
    # Find all Proxy characters that have the same lodestone ID as this one
    proxies = Character.objects.filter(user__isnull=True, lodestone_id=real_char.lodestone_id)

    # For each Character (which should only ever be in one team each);
    #   - Notify the Team Leader that the claim has happened
    #   - Move the BIS List to the real Character, name it using the Team's name
    #   - Update the TeamMember object to point to this character
    for char in proxies:
        for tm in char.teammember_set.all():
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
    err = xivapi_lookup(obj.lodestone_id, obj.token, logger)
    logger.debug('finished lookup function')

    if err is not None:
        notifier.verify_fail(obj, err)
        logger.info(f'Character #{pk} could not be verified. Exiting.')
        return

    logger.info(f'Character #{pk} verified. Updating DB.')
    # First we update the flag on the object specified
    obj.verified = True
    obj.save()

    # Before we go deleting any Characters, we need to sort all the Proxies that share the lodestone ID
    assimilate_proxies(obj)

    # Next delete all unverified instances of the character (this includes proxies)
    logger.debug(f'Deleting unverified instances of Character #{obj.lodestone_id} (#{pk}).')
    objs = Character.objects.filter(verified=False, lodestone_id=obj.lodestone_id).exclude(pk=pk)
    logger.debug(f'Found {objs.count()} instances of Character #{obj.lodestone_id} to delete.')
    objs.delete()
    # Then we're done!
    notifier.verify_success(obj)
    # Also send websocket details
    channel_layer = get_channel_layer()
    if channel_layer is not None:
        async_to_sync(channel_layer.group_send)(f'user-updates-{obj.user.id}', {'type': 'character', 'id': obj.pk})


@shared_task(name='cleanup')
def cleanup():
    """
    Cleanup the DB of all unverified (non-proxy) characters made more than 24h ago
    """
    logger.debug(f'Running at: {timezone.now()}')
    older_than = timezone.now() - timedelta(hours=24)
    logger.debug(f'Deleting unverified characters older than {older_than}.')

    objs = Character.objects.filter(verified=False, user__isnull=False, created__lt=older_than)
    logger.debug(f'Found {objs.count()} characters. Deleting them.')
    objs.delete()
