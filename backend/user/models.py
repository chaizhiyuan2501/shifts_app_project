from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """ユーザー管理用マネージャークラス"""

    def create_user(self, name, password=None, email=None, **extra_fields):
        """
        一般ユーザーを作成するメソッド。
        - 名前は必須
        - パスワードをハッシュ化して保存
        - オプションでメールアドレスも保存
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
        """
        管理者ユーザー（スーパーユーザー）を作成するメソッド。
        - is_admin, is_staff, is_superuser をTrueに設定
        """
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
    """カスタムユーザーモデル（出勤管理システム用）"""

    name = models.CharField(
        max_length=255, unique=True, verbose_name="表示名"
    )  # ユーザー名（ユニーク制約あり）
    email = models.EmailField(
        max_length=255,
        unique=True,
        blank=True,
        null=True,
        verbose_name="メールアドレス",
    )  # メールアドレス（任意）
    is_admin = models.BooleanField(default=False, verbose_name="管理者フラグ")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Userモデルに紐付くマネージャー
    objects = UserManager()

    # ログイン時に使用するフィールド
    USERNAME_FIELD = "name"
    REQUIRED_FIELDS = []  # スーパーユーザー作成時の必須項目（ここではなし）

    class Meta:
        db_table = "user"  # 実際にDBで使うテーブル名
        verbose_name = "ユーザー"  # Django管理画面での単数形表示
        verbose_name_plural = "ユーザー"  # Django管理画面での複数形表示

    def __str__(self):
        """管理画面などで表示される文字列"""
        return f"{self.name}（管理者）" if self.is_admin else self.name
