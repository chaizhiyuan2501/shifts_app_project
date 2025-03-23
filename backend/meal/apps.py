from django.apps import AppConfig


class MealConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "meal"

    def ready(self):
        # アプリ起動時に signals を読み込む
        from . import signals
