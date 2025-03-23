# meal/signals.py

from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import MealType


@receiver(post_migrate)
def create_default_meal_types(sender, **kwargs):
    """
    デフォルトの食事種類（朝・昼・夕）を自動登録。
    """
    if sender.name != "meal":
        return

    default_meals = [
        {"name": "朝", "display_name": "朝食"},
        {"name": "昼", "display_name": "昼食"},
        {"name": "夕", "display_name": "夕食"},
    ]

    for meal in default_meals:
        obj, created = MealType.objects.get_or_create(
            name=meal["name"],
            defaults={
                "display_name": meal["display_name"]
            }
        )
        if created:
            print(f"[Init] MealType '{meal['display_name']}' を作成しました。")
