from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


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
    # avatar=models.ImageField(upload_to=avatar_image_file_path,null=True,blank=True,verbose_name="アバター")
    email = models.EmailField(
        max_length=255, unique=True, verbose_name="メールアドレス"
    )
    is_active = models.BooleanField(default=True, verbose_name="ユーザーの有効状態")
    is_staff = models.BooleanField(default=False, verbose_name="スタッフ権限")

    objects = UserManager()

    USERNAME_FIELD = "email"  # ユーザーを一意に識別するフィールドの指定

    class Meta:
        db_table = "User"
        verbose_name = "ユーザー"

    def __srt__(self):
        return self.name


class Staff(models.Model):
    pass


class Guest(models.Model):
    pass


class StaffSchedule(models.Model):
    pass


class GuestSchedule(models.Model):
    pass
