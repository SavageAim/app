# lib
import requests
from django.conf import settings
from django.core.management.base import BaseCommand
# local
from api import models

HEADERS = {'User-Agent': 'savageaim.com'}


class Command(BaseCommand):
    help = 'Check if the system has imported all of the present versions in XIVAPI'

    def add_arguments(self, parser):
        parser.add_argument('--latest', action='store_true')
        parser.add_argument('--notify', action='store_true')

    def handle(self, latest=False, notify=False, *args, **options):
        # List the API versions from the server, check what are in the DB, and write the message / webhook payload
        response = requests.get('https://v2.xivapi.com/api/version', headers=HEADERS)
        response.raise_for_status()

        api_versions = set()
        for result in response.json()['versions']:
            names = result['names']
            if latest and 'latest' not in names:
                continue

            for name in names:
                if name != 'latest':
                    api_versions.add(name)

        # Fetch the seeded versions from the DB
        seeded_versions = set(models.XIVVersion.objects.values_list('version', flat=True))
        unseeded_versions = api_versions - seeded_versions
        if not unseeded_versions:
            # If we have none, we can just leave here
            return

        if notify:
            self.send_webhook_payload(unseeded_versions)
        else:
            print('Found Unseeded Versions')
            for version in sorted(unseeded_versions):
                print(f'- {version}')

    def send_webhook_payload(self, unseeded_versions: set[str]):
        if settings.VERSION_WEBHOOK is None:
            return
        lines = ['Unseeded Versions Found;', '```']
        lines.extend(sorted(unseeded_versions))
        lines.append('```')
        payload = {
            'content': '\n'.join(lines),
        }
        response = requests.post(settings.VERSION_WEBHOOK, json=payload)
        if not response.ok:
            print(response.text)
        response.raise_for_status()
