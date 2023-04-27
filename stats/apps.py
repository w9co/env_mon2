from django.apps import AppConfig
from . import tasks


class StatsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stats'

    def ready(self):
        from .tasks import start
        start();
