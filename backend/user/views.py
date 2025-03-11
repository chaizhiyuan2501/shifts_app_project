from django.contrib.auth import get_user_model


from rest_framework import generics, authentication, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.settings import api_settings

from utils.validators import is_invalid_password_format, is_invalid_email_format

from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
)


class CreateUserView(generics.CreateAPIView):
    """新しいユーザーを作成する"""

    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """ユーザーの新しい認証用トークンを作成する"""

    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """認証されたユーザーを管理する"""

    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """認証されたユーザーを取得する"""
        return self.request.user
