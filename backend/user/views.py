from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .serializers import RegisterUserSerializer, UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.utils import extend_schema
from .serializers import CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@extend_schema(
    summary="ユーザー登録（管理者のみ）",
    description="管理者が新しいユーザーを登録します。名前、メールアドレス、パスワードが必要です。",
    tags=["ユーザー管理"],
)
@api_view(["POST"])
@permission_classes([AllowAny])
def register_user(request):
    """
    ユーザー登録（登録後JWTトークン返す）
    """
    serializer = RegisterUserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()

        from rest_framework_simplejwt.tokens import RefreshToken

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "user": UserSerializer(user).data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    summary="ユーザー情報取得",
    description="ユーザーの基本情報",
    tags=["ユーザー管理"],
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def current_user_info(request):
    """
    現在ログイン中のユーザー情報
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@extend_schema(
    summary="JWT ログイン",
    description="ユーザー名（name）とパスワードでログインし、access・refreshトークンを取得します。",
    tags=["認証"],
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "example": "田中"},
                "password": {"type": "string", "example": "1980"},
            },
        }
    },
    responses={
        200: {
            "type": "object",
            "properties": {
                "refresh": {"type": "string"},
                "access": {"type": "string"},
                "user": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "name": {"type": "string"},
                        "email": {"type": "string"},
                        "role": {"type": "string"},
                        "is_admin": {"type": "boolean"},
                    },
                },
            },
        }
    },
)
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@extend_schema(
    summary="アクセストークン更新",
    description="refreshトークンを使って新しいaccessトークンを取得します。",
    tags=["認証"],
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "refresh": {"type": "string", "example": "xxxxx.yyyyy.zzzzz"},
            },
        }
    },
    responses={
        200: {
            "type": "object",
            "properties": {
                "access": {"type": "string"},
            },
        }
    },
)
class CustomTokenRefreshView(TokenRefreshView):
    pass
