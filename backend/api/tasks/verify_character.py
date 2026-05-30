from io import StringIO

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.conf import settings
from django.db.models import Q
from django_cloud_tasks.serializers import serialize
from django_cloud_tasks.tasks import SubscriberTask

from .base import SavageAimPublisherTask
from .. import notifier
from ..lodestone_scraper import LodestoneScraper
from ..models import Character

TOPIC_NAME = 'verify-character'


class VerifyCharacterTask(SavageAimPublisherTask):

    @classmethod
    def topic_name(cls) -> str:
        return TOPIC_NAME


class VerifyCharacterTaskSubscriber(SubscriberTask):

    @classmethod
    def topic_name(cls) -> str:
        return TOPIC_NAME

    def _assimilate_proxies(self, real_char: Character):
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

    def run(self, content: dict, output: StringIO | None = None, *args, **kwargs) -> dict:
        pk = content['pk']
        print(f'Commencing verification attempt for Character #{pk}', file=output)
        try:
            obj = Character.objects.get(pk=pk, verified=False)
        except Character.DoesNotExist:
            print(f'Character #{pk} either does not exist, or is already verified.', file=output)
            return {'status': 'verified', 'already': 'yes'}

        print('calling lookup function', file=output)
        err = LodestoneScraper.get_instance().check_token(obj.lodestone_id, obj.token)
        print('finished lookup function', file=output)

        if err is not None:
            notifier.verify_fail(obj, err)
            print(f'Character #{pk} could not be verified. Error: {err}', file=output)
            return {'status': 'failed', 'error': err}

        print(f'Character #{pk} verified. Updating DB.', file=output)
        obj.verified = True
        obj.save()

        # Assimilate proxies to add this character to its Teams
        self._assimilate_proxies(obj)

        # Finally cleanup the DB
        print(
            f'Deleting unverified instances of Character #{obj.lodestone_id} (#{obj.pk}) owned by {obj.user_id}.',
            file=output,
        )
        objs = Character.objects.filter(
            Q(user__isnull=True) | Q(user_id=obj.user_id),
            verified=False,
            lodestone_id=obj.lodestone_id,
        ).exclude(pk=pk)
        ids_to_delete = [o.pk for o in objs]
        print(
            f'Found {objs.count()} instances of Character #{obj.lodestone_id} to delete.\n{ids_to_delete}',
            file=output,
        )
        objs.delete()
        # Then we're done!
        notifier.verify_success(obj)
        # Also send websocket details
        channel_layer = get_channel_layer()
        if channel_layer is not None:
            async_to_sync(channel_layer.group_send)(f'user-updates-{obj.user.id}', {'type': 'character', 'id': obj.pk})

        return {'status': 'verified', 'already': 'no'}
