from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Role


class StaffConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "staff"


@receiver(post_migrate)
def create_default_role(self, **kwargs):
    default_role = ["正社員", "アルバイト", "夜勤専門"]
    for role_name in default_role:
        Role.objects.get_or_create(name=role_name)
