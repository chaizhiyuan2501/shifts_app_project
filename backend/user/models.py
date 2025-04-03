from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """ユーザーのマネージャーモデル"""

    def create_user(self, name, password=None, email=None, **extra_fields):
        """
        一般ユーザー作成（名前 + パスワード、管理者の場合はメールも使用可能）
        """
        if not name:
            raise ValueError("ユーザー名は必須です。")

        user = self.model(
            name=name,
            email=self.normalize_email(email) if email else None,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, password, email=None, **extra_fields):
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(
            name=name,
            password=password,
            email=email,
            **extra_fields,
        )


class User(AbstractBaseUser, PermissionsMixin):
    """出勤管理システム用のユーザーモデル"""

    name = models.CharField(
        max_length=255, unique=True, verbose_name="表示名"
    )  # ユニークにする
    email = models.EmailField(
        max_length=255,
        unique=True,
        blank=True,
        null=True,
        verbose_name="メールアドレス",
    )
    is_admin = models.BooleanField(default=False, verbose_name="管理者フラグ")
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "name"  # ← 名前でログイン
    REQUIRED_FIELDS = []  # superuser 用には別途指定

    class Meta:
        db_table = "user"
        # Django管理サイトで表示される単数形の名称（例：「ユーザーを追加」など）
        verbose_name = "ユーザー"
        # Django管理サイトで表示される複数形の名称（例：「ユーザー一覧」など）
        # ※省略すると「ユーザーs」になってしまうため、明示的に指定
        verbose_name_plural = "ユーザー"

    def __str__(self):
        return f"{self.name}（管理者）" if self.is_admin else self.name
