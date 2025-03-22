"""
データベースモデル
"""

from django.db import models
import uuid
import os

from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

from utils.db import BaseModel


class UserManager(BaseUserManager):
    """ユーザーのマネージャーモデル"""

    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        """新しいユーザー作成し､保存する"""
        if not email:
            raise ValueError("メールアドレスが必要です｡")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """ユーザーモデル"""

    name = models.CharField(max_length=255, blank=False, verbose_name="ユーザーネーム")
    email = models.EmailField(
        max_length=255, unique=True, verbose_name="メールアドレス"
    )
    is_active = models.BooleanField(default=True, verbose_name="ユーザーの有効状態")
    role = models.CharField(max_length=50)
    is_admin = models.BooleanField(default=False, verbose_name="管理者の状態")

    objects = UserManager()

    USERNAME_FIELD = "name"  # ユーザーを一意に識別するフィールドの指定

    class Meta:
        db_table = "User"
        verbose_name = "ユーザー"

    def __srt__(self):
        return self.name
