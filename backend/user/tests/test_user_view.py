import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from user.models import User


@pytest.mark.django_db
class TestUserAPIViews:
    """
    User関連APIのテストクラス
    """

    def setup_method(self):
        """
        テスト前準備
        - データベースを初期化
        - APIClientの初期化
        """
        User.objects.all().delete()
        self.client = APIClient()
        self.register_url = reverse("user:user-register")
        self.login_url = reverse("user:user-login")
        self.user_list_url = reverse("user:user-list")
        self.user = User.objects.create_user(name="testuser", password="1980")
        self.admin = User.objects.create_superuser(name="admin", password="adminpass")

    def test_user_register(self):
        """
        ユーザー登録APIのテスト
        - 正しいリクエストで201レスポンスを返す
        """
        data = {"name": "newuser", "password": "1234"}
        response = self.client.post(self.register_url, data, format="json")
        assert response.status_code == 201
        assert response.data["data"]["name"] == "newuser"

    def test_user_login(self):
        """
        ログインAPIのテスト
        - 正しい認証情報でログインでき、トークンが返る
        """
        data = {"name": "testuser", "password": "1980"}
        response = self.client.post(self.login_url, data, format="json")
        assert response.status_code == 200
        assert "access" in response.data["data"]
        assert "refresh" in response.data["data"]
        self.access_token = response.data["data"]["access"]

    def test_user_list_authenticated(self):
        """
        ユーザー一覧取得API（認証あり）のテスト
        """
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.user_list_url)
        assert response.status_code == 200
        assert isinstance(response.data["data"], list)

    def test_user_list_unauthenticated(self):
        """
        ユーザー一覧取得API（認証なし）のテスト
        - 401エラーになること
        """
        response = self.client.get(self.user_list_url)
        assert response.status_code == 401

    def test_user_detail_get(self):
        """
        ユーザー詳細取得APIのテスト
        - 正常に取得できること
        """
        self.client.force_authenticate(user=self.user)
        url = reverse("user:user-detail", kwargs={"id": self.user.id})
        response = self.client.get(url)
        assert response.status_code == 200
        assert response.data["data"]["name"] == self.user.name

    def test_user_update(self):
        """
        ユーザー情報更新APIのテスト
        - 名前を更新できること
        """
        self.client.force_authenticate(user=self.user)
        url = reverse("user:user-detail", kwargs={"id": self.user.id})
        data = {"name": "updateduser"}
        response = self.client.put(url, data, format="json")
        assert response.status_code == 200
        assert response.data["data"]["name"] == "updateduser"

    def test_user_delete(self):
        """
        ユーザー削除APIのテスト
        - 管理者が削除できること
        """
        self.client.force_authenticate(user=self.admin)
        url = reverse("user:user-detail", kwargs={"id": self.user.id})
        response = self.client.delete(url)
        assert response.status_code == 204
