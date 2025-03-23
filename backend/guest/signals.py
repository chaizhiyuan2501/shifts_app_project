from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import VisitType


@receiver(post_migrate)
def create_default_visit_types(sender, **kwargs):
    """
    デフォルトの来訪種別（泊、通い、休）を自動登録する。
    """
    # app名をフィルタして他のappのmigrate時には実行しない
    if sender.name != "guest":
        return

    default_visit_types = [
        {"code": "泊", "name": "泊まり", "color": "#3498db"},   # 蓝色
        {"code": "通い", "name": "通い", "color": "#2ecc71"},  # 绿色
        {"code": "休", "name": "休み", "color": "#e74c3c"},    # 红色
    ]

    for visit in default_visit_types:
        VisitType.objects.get_or_create(
            code=visit["code"],
            defaults={
                "name": visit["name"],
                "color": visit["color"]
            }
        )
