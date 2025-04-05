import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from user.models import User


@pytest.mark.django_db
class TestUserAPIViews:
    def setup_method(self):
        User.objects.all().delete()  # テストケースごとにデータの重複や干渉を防ぐため、ユーザーモデルの全データを削除し、クリーンな状態から開始する。
        self.client = APIClient()
        self.register_url = reverse("user:user-register")
        self.login_url = reverse("user:user-login")
        self.user_list_url = reverse("user:user-list")
        self.user = User.objects.create_user(name="testuser", password="1980")
        self.admin = User.objects.create_superuser(name="admin", password="adminpass")

    def test_user_register(self):
        """
        ユーザー登録APIのテスト
        - 正しいnameとpasswordでユーザーが登録されること
        """
        data = {"name": "newuser", "password": "1234"}
        response = self.client.post(self.register_url, data, format="json")
        assert response.status_code == 201
        assert response.data["data"]["name"] == "newuser"

    def test_user_login(self):
        """
        ログインAPIのテスト
        - 登録済みユーザーでログインできること
        - アクセストークンとリフレッシュトークンが返されること
        """
        data = {"name": "testuser", "password": "1980"}
        response = self.client.post(self.login_url, data, format="json")
        assert response.status_code == 200
        assert "access" in response.data["data"]
        assert "refresh" in response.data["data"]
        self.access_token = response.data["data"]["access"]

    def test_user_list_authenticated(self):
        """
        ユーザー一覧APIのテスト（認証あり）
        - アクセストークン付きでアクセスできること
        """
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.user_list_url)
        assert response.status_code == 200
        assert isinstance(response.data["data"], list)

    def test_user_list_unauthenticated(self):
        """
        ユーザー一覧APIのテスト（認証なし）
        - 認証していない場合は401エラーになること
        """
        response = self.client.get(self.user_list_url)
        assert response.status_code == 401

    def test_user_detail_get(self):
        """
        ユーザー詳細取得APIのテスト
        - 自身または管理者がユーザー詳細を取得できること
        """
        self.client.force_authenticate(user=self.user)
        url = reverse("user:user-detail", kwargs={"id": self.user.id})
        response = self.client.get(url)
        assert response.status_code == 200
        assert response.data["data"]["name"] == self.user.name

    def test_user_update(self):
        """
        ユーザー更新APIのテスト
        - ユーザー名を変更できること
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
        - 管理者がユーザーを削除できること
        """
        self.client.force_authenticate(user=self.admin)
        url = reverse("user:user-detail", kwargs={"id": self.user.id})
        response = self.client.delete(url)
        assert response.status_code == 204
