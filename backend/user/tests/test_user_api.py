import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse

from user.models import User


# テスト用のAPIクライアント
@pytest.fixture
def api_client():
    return APIClient()


USER_REGISTER_URL = reverse("user:register")
USER_LOGIN_URL = reverse("user:token_obtain_pair")


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


# 管理者ユーザーを作成
@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(name="admin", password="1993")


# トークンを取得するフィクスチャ
@pytest.fixture
def get_token(api_client, admin_user):
    response = api_client.post(
        reverse("token_obtain_pair"), {"name": "admin", "password": "1980"}
    )
    return response.data["access"]


# ログインAPIのテスト（JWTトークン取得）
@pytest.mark.django_db
def test_login_user(api_client):
    User.objects.create_user(name="loginuser", password="1980")
    response = api_client.post(
        USER_LOGIN_URL, {"name": "loginuser", "password": "1980"}
    )
    assert response.status_code == 200
    assert "access" in response.data


@pytest.mark.django_db
# このクラスの中で「データベースアクセス」があることを pytest に知らせるマーク
# これがないと、データベースを使ったテストがブロックされてしまう
# 例えば、ユーザー登録・ログイン・モデル作成などはすべてDB操作になるので必要
class TestPublicUserAPI:
    """
    認証不要のユーザーAPIをテストするクラス。
    例：ユーザー登録、ログイン、パスワード確認など。
    pytest で自動認識されるようにクラス名は「Test」で始めること。
    """

    def setup_method(self):
        self.client = APIClient()

    # ユーザー登録APIのテスト
    def test_register_user(self):
        # ユーザー登録APIへPOSTリクエスト（名前とパスワードを送信）
        response = self.client.post(
            USER_REGISTER_URL,
            {
                "name": "testuser",  # ユーザー名（4桁パスワードでログインする想定）
                "password": "1980",  # パスワード（生年月日の下4桁など）
            },
        )

        # ステータスコードが 201 Created であることを確認
        assert response.status_code == 201

        # レスポンスの中に含まれる「user.name」が正しく設定されているか確認
        assert response.data["user"]["name"] == "testuser"

        # JWTのアクセストークンが含まれていることを確認
        assert "access" in response.data

        # JWTのリフレッシュトークンが含まれていることを確認
        assert "refresh" in response.data

    # ログインAPIのテスト（JWTトークン取得）
    def test_login_user(self):
        User.objects.create_user(name="loginuser", password="1980")
        response = self.client.post(
            USER_LOGIN_URL, {"name": "loginuser", "password": "1980"}
        )
        assert response.status_code == 200
        assert "access" in response.data


@pytest.mark.django_db
class TestPrivateUserAPI:
    """
    認証が必要なユーザーAPIをテストするクラス。
    例えば、現在のユーザー情報取得（/me）、ユーザー情報更新など。
    """

    def setup_method(self):
        """
        各テストメソッドの前に実行される初期化処理。
        テストユーザーを作成し、そのユーザーとして認証状態でAPIClientをセット。
        """
        self.user = create_user(
            name="testuser", password="1980"
        )  # テスト用ユーザーを作成
        self.client = APIClient()  # DRFのテスト用クライアントを初期化
        self.client.force_authenticate(
            user=self.user
        )  # このユーザーで強制ログイン（認証付きAPIをテストできる）
