from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model


@receiver(post_migrate)
def create_default_admin(sender, **kwargs):
    """
    デフォルトの管理者ユーザーを作成
    """
    User = get_user_model()
    if not User.objects.filter(name="admin").exists():
        User.objects.create_superuser(
            name="admin",
            password="1993",
            email="admin@mail.com",
            is_admin=True,
        )
        print("初期管理者 admin が作成されました.")
