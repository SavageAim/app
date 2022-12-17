from datetime import timedelta
import requests
from allauth.socialaccount.models import SocialApp, SocialToken
from django.core.management.base import BaseCommand
from django.utils import timezone

THRESHOLD_HOURS = 24
URL = 'https://discord.com/api/oauth2/token'


class Command(BaseCommand):
    help = 'Refresh any discord oauth tokens that are expiring within the threshold'

    def handle(self, *args, **kwargs):
        # We only have one social app
        app = SocialApp.objects.first()

        # First, get all social tokens that expire within the threshold
        current_time = timezone.now()
        expiry_threshold = current_time + timedelta(hours=THRESHOLD_HOURS)
        self.stdout.write(f'Searching for tokens expiring between {current_time} and {expiry_threshold}')
        to_refresh = SocialToken.objects.filter(expires_at__lte=expiry_threshold, expires_at__gte=current_time)
        self.stdout.write(f'Found {to_refresh.count()} tokens')

        # Loop through refreshable tokens and make requests
        for token in to_refresh:
            refresh_data = {
                'grant_type': 'refresh_token',
                'client_id': app.client_id,
                'client_secret': app.secret,
                'refresh_token': token.token_secret,
            }
            self.stdout.write(f'Refreshing token for {token.account.user.username}')

            response = requests.post(URL, refresh_data)
            if response.status_code != 200:
                self.stderr.write(f'Token refresh failed: {response.content}')
                continue

            # Save the updated data for the token
            response_data = response.json()
            token.token = response_data['access_token']
            token.token_secret = response_data['refresh_token']
            token.expires_at = timezone.now() + timedelta(seconds=response_data['expires_in'])
            token.save()
