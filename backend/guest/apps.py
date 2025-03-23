from django.apps import AppConfig
from django.db.models.signals import post_migrate

class GuestConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'guest'

    def ready(self):
        # アプリ起動時に signals を登録
        from . import signals