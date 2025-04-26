import pytest
from user.models import User
from django.db.utils import IntegrityError
import uuid


@pytest.mark.django_db
class TestUserModel:
    """
    Userモデルのテストクラス。
    - 一般ユーザーと管理者ユーザーの作成テスト
    - __str__出力確認
    - 制約違反（例：名前の重複）のテスト
    """

    def test_create_general_user(self):
        """
        一般ユーザー作成のテスト
        - ユーザー名が正しく保存されること
        - パスワード検証が通ること
        - is_admin, is_staff が Falseであること
        """
        user = User.objects.create_user(name="newuser", password="1234")
        assert user.name == "newuser"
        assert user.check_password("1234")
        assert user.is_admin is False
        assert user.is_staff is False

    def test_create_superuser(self):
        """
        スーパーユーザー作成のテスト
        - is_admin, is_superuser, is_staffがTrueであること
        """
        admin = User.objects.create_superuser(name="super", password="5678")
        assert admin.is_admin is True
        assert admin.is_superuser is True
        assert admin.is_staff is True

    def test_user_str_method(self):
        """
        __str__メソッドの出力確認
        - 通常ユーザーは名前のみ
        - 管理者ユーザーは「（管理者）」が付く
        """
        user = User.objects.create_user(
            name=f"user_{uuid.uuid4().hex[:6]}", password="1234"
        )
        admin = User.objects.create_superuser(
            name=f"admin_{uuid.uuid4().hex[:6]}", password="5678"
        )
        assert str(user) == user.name
        assert str(admin) == f"{admin.name}（管理者）"

    def test_user_requires_name(self):
        """
        nameが空の場合、ValueErrorが発生することを確認する
        """
        with pytest.raises(ValueError) as e:
            User.objects.create_user(name="", password="1980")
        assert "ユーザー名は必須" in str(e.value)

    def test_email_can_be_null(self):
        """
        emailが未設定（null）でもユーザー作成できること
        """
        user = User.objects.create_user(name="noemail", password="1980")
        assert user.email is None

    def test_duplicate_username_raises_error(self):
        """
        ユーザー名が重複した場合、IntegrityErrorが発生すること
        """
        User.objects.create_user(name="duplicate", password="1980")
        with pytest.raises(IntegrityError):
            User.objects.create_user(name="duplicate", password="1980")
