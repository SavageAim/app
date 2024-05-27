"""
Celery settings and definition and stuff
"""

import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings


# setup the settings (live is copied over settings file in docker)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Create and set up the celery app
app = Celery('savageaim')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Set up celery beat for deleting unverified users after 24h ish
app.conf.beat_schedule = {
    'cleanup_unverified_characters': {
        'task': 'cleanup',
        'schedule': crontab(minute=0),
    },
    'remind_to_verify': {
        'task': 'verify_reminder',
        'schedule': crontab(minute=0),
    },
    'refresh_oauth_tokens': {
        'task': 'refresh_tokens',
        'schedule': crontab(hour=0, minute=0),
    }
}
