"""
WSGI config for backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
# Import all tasks here to get them picked up by the wsgi applications
from api.tasks import *  # noqa


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')


application = get_wsgi_application()
