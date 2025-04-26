"""
user アプリ用 Views
 - model / serializer_class を各 View に保持し、可読性と保守性を向上
 - POST・PUT だけ request=Serializer を残す
 - 日本語コメントを詳細に付記
"""

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken

from .models import User
from .serializers import (
    RegisterUserSerializer,
    UserSerializer,
    CustomTokenObtainPairSerializer,
)
from utils.api_response_utils import api_response


# ================================================================
# ユーザー登録
# ================================================================
class UserRegisterView(APIView):
    """ユーザー新規登録"""

    permission_classes = [AllowAny]
    model = User
    serializer_class = RegisterUserSerializer

    @extend_schema(
        operation_id="UserRegister",
        summary="ユーザー登録",
        tags=["ユーザー管理"],
        request=RegisterUserSerializer,  # 登録に必要な項目を表示
        responses={
            201: OpenApiResponse(description="ユーザー登録成功"),
            400: OpenApiResponse(description="バリデーションエラー"),
        },
    )
    def post(self, request):
        ser = self.serializer_class(data=request.data)
        if ser.is_valid():
            ser.save()
            return api_response(
                data=ser.data,
                code=201,
                message="ユーザー登録成功",
                status_code=status.HTTP_201_CREATED,
            )
        return api_response(
            message="バリデーションエラー",
            code=400,
            data=ser.errors,
            status_code=status.HTTP_400_BAD_REQUEST,
        )


# ================================================================
# ユーザー一覧
# ================================================================
class UserListView(APIView):
    """ユーザー一覧取得"""

    permission_classes = [IsAuthenticated]
    model = User
    serializer_class = UserSerializer

    @extend_schema(
        operation_id="UserList",
        summary="ユーザー一覧取得",
        tags=["ユーザー管理"],
        responses={200: OpenApiResponse(description="ユーザー一覧取得成功")},
    )
    def get(self, request):
        users = self.model.objects.all()
        ser = self.serializer_class(users, many=True)
        return api_response(data=ser.data, message="ユーザー一覧取得成功")


# ================================================================
# ユーザー詳細・更新・削除
# ================================================================
class UserDetailView(APIView):

    permission_classes = [IsAuthenticated]
    model = User
    serializer_class = UserSerializer

    def get_object(self, pk):
        """IDから対象ユーザーを取得"""
        return get_object_or_404(self.model, pk=pk)

    @extend_schema(
        operation_id="UserRetrieve",
        summary="ユーザー詳細取得",
        tags=["ユーザー管理"],
        responses={
            200: OpenApiResponse(description="詳細取得成功"),
            404: OpenApiResponse(description="該当ユーザーなし"),
        },
    )
    def get(self, request, *args, **kwargs):
        """ユーザー詳細取得API"""
        pk = kwargs.get("id")
        user = self.get_object(pk)
        serializer = self.serializer_class(user)
        return api_response(data=serializer.data, message="ユーザー詳細取得成功")

    @extend_schema(
        operation_id="UserUpdate",
        summary="ユーザー更新",
        tags=["ユーザー管理"],
        request=UserSerializer,
        responses={
            200: OpenApiResponse(description="更新成功"),
            400: OpenApiResponse(description="バリデーションエラー"),
        },
    )
    def put(self, request, *args, **kwargs):
        """ユーザー更新API"""
        pk = kwargs.get("id")
        user = self.get_object(pk)
        serializer = self.serializer_class(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return api_response(data=serializer.data, message="ユーザー更新成功")
        return api_response(
            message="バリデーションエラー", code=400, data=serializer.errors
        )

    @extend_schema(
        operation_id="UserDelete",
        summary="ユーザー削除",
        tags=["ユーザー管理"],
        responses={
            204: OpenApiResponse(description="削除成功"),
            404: OpenApiResponse(description="該当ユーザーなし"),
        },
    )
    def delete(self, request, *args, **kwargs):
        """ユーザー削除API"""
        pk = kwargs.get("id")
        user = self.get_object(pk)
        user.delete()
        return api_response(message="ユーザー削除成功", code=204)


# ================================================================
# JWT ログイン
# ================================================================
class CustomTokenObtainPairView(TokenObtainPairView):
    """JWT ログイン（カスタムSerializer）"""

    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]

    @extend_schema(
        operation_id="TokenObtainPair",
        summary="JWTログイン",
        tags=["認証"],
        responses={
            200: OpenApiResponse(description="ログイン成功"),
            401: OpenApiResponse(description="認証失敗"),
        },
    )
    def post(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data)
        try:
            ser.is_valid(raise_exception=True)
        except Exception as e:
            return api_response(
                message="認証失敗",
                code=401,
                data=str(e),
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        return api_response(data=ser.validated_data, message="ログイン成功")


# ================================================================
# リフレッシュトークンでアクセストークン再発行
# ================================================================
class CustomTokenRefreshView(APIView):
    """リフレッシュトークンでアクセストークン更新"""

    permission_classes = [AllowAny]

    @extend_schema(
        operation_id="TokenRefresh",
        summary="アクセストークン更新",
        tags=["認証"],
        responses={
            200: OpenApiResponse(description="更新成功"),
            401: OpenApiResponse(description="無効トークン"),
        },
    )
    def post(self, request):
        serializer = TokenRefreshSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except InvalidToken as e:
            return api_response(
                message="無効なリフレッシュトークン",
                code=401,
                data=str(e),
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        return api_response(data=serializer.validated_data, message="更新成功")
