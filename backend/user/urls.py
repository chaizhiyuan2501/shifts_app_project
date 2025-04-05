from django.urls import path
from .views import (
    UserRegisterView,
    UserListView,
    UserDetailView,
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
)

app_name = 'user'

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="user-register"),         # ユーザー登録
    path("login/", CustomTokenObtainPairView.as_view(), name="user-login"),      # JWTログイン（アクセストークン + リフレッシュトークン）
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="token-refresh"),  # アクセストークン再発行
    path("users/", UserListView.as_view(), name="user-list"),                    # ユーザー一覧
    path("users/<int:id>/", UserDetailView.as_view(), name="user-detail"),       # ユーザー詳細
]
