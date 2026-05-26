from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = 'api'
    default_auto_field = 'django.db.models.AutoField'

    def ready(self):
        # Import all our cloud tasks in here so they can be discovered
        from api.tasks import *  # noqa
