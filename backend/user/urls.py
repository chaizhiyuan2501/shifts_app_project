from django.urls import path
from .views import (
    UserRegisterView,
    UserListView,
    UserDetailView,
    CustomTokenObtainPairView,
)
from .views import CustomTokenObtainPairView, CustomTokenRefreshView

app_name = 'user'

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="user-register"),
    path("login/", CustomTokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("users/", UserListView.as_view(), name="user-list"),
    path("users/<int:id>/", UserDetailView.as_view(), name="user-detail"),
    # JWT 認証用
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
]
