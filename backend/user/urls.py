from django.urls import path
from .views import (
    register_user,
    current_user_info,
    CustomTokenObtainPairView,
)
from .views import CustomTokenObtainPairView, CustomTokenRefreshView

app_name = 'user'

urlpatterns = [
    path("register/", register_user, name="register"),
    path("me/", current_user_info, name="me"),
    # JWT 認証用
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
]
