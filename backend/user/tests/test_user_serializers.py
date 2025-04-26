import pytest
from user.models import User
from user.serializers import (
    RegisterUserSerializer,
    UserSerializer,
    CustomTokenObtainPairSerializer,
)
from rest_framework.exceptions import ValidationError


@pytest.mark.django_db
class TestRegisterUserSerializer:
    """
    RegisterUserSerializer のテストクラス。
    - ユーザー登録のバリデーションチェック
    """

    def test_valid_data(self):
        """
        正しいデータでユーザー登録が成功すること
        """
        data = {"name": "新ユーザー", "password": "1234"}
        serializer = RegisterUserSerializer(data=data)
        assert serializer.is_valid() is True
        user = serializer.save()
        assert user.name == "新ユーザー"
        assert user.check_password("1234")

    def test_name_is_required(self):
        """
        nameが空の場合にバリデーションエラーが発生すること
        """
        data = {"name": "", "password": "1234"}
        serializer = RegisterUserSerializer(data=data)
        assert serializer.is_valid() is False
        assert "name" in serializer.errors

    def test_name_must_be_at_least_2_characters(self):
        """
        nameが2文字未満の場合にバリデーションエラーが発生すること
        """
        data = {"name": "あ", "password": "1234"}
        serializer = RegisterUserSerializer(data=data)
        assert serializer.is_valid() is False
        assert "name" in serializer.errors

    def test_name_must_be_unique(self):
        """
        nameが重複している場合にバリデーションエラーが発生すること
        """
        User.objects.create_user(name="testuser", password="pass")
        data = {"name": "testuser", "password": "newpass"}
        serializer = RegisterUserSerializer(data=data)
        assert serializer.is_valid() is False
        assert "name" in serializer.errors

    def test_password_required(self):
        """
        passwordが空の場合にバリデーションエラーが発生すること
        """
        data = {"name": "user2", "password": ""}
        serializer = RegisterUserSerializer(data=data)
        assert serializer.is_valid() is False
        assert "password" in serializer.errors


@pytest.mark.django_db
class TestUserSerializer:
    """
    UserSerializer のテストクラス。
    - 出力専用のテスト
    """

    def test_user_serialization(self):
        """
        ユーザーオブジェクトを正しくシリアライズできること
        """
        user = User.objects.create_user(name="田中一郎", password="1980")
        serializer = UserSerializer(user)
        assert serializer.data["name"] == "田中一郎"
        assert "password" not in serializer.data


@pytest.mark.django_db
class TestCustomTokenObtainPairSerializer:
    """
    CustomTokenObtainPairSerializer のテストクラス。
    """

    def test_valid_login(self):
        """
        正しい認証情報でトークンが取得できること
        """
        User.objects.create_user(name="loginuser", password="1980")
        data = {"name": "loginuser", "password": "1980"}
        serializer = CustomTokenObtainPairSerializer(data=data)
        assert serializer.is_valid()
        tokens = serializer.validated_data
        assert "access" in tokens
        assert "refresh" in tokens

    def test_invalid_login(self):
        """
        間違ったパスワードの場合に認証エラーが発生すること
        """
        User.objects.create_user(name="loginuser", password="1980")
        data = {"name": "loginuser", "password": "wrong"}
        serializer = CustomTokenObtainPairSerializer(data=data)
        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)
