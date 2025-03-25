from django.urls import path
from .views import (
    register_user,
    current_user_info,
    CustomTokenObtainPairView,
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("register/", register_user, name="register"),
    path("me/", current_user_info, name="me"),
    # JWT 認証用
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
