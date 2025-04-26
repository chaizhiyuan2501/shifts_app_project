from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken
from django.shortcuts import get_object_or_404

from .models import User
from .serializers import (
    RegisterUserSerializer,
    UserSerializer,
    CustomTokenObtainPairSerializer,
)
from utils.api_response_utils import api_response


@extend_schema(
    summary="ユーザー登録",
    tags=["ユーザー管理"],
    responses={
        201: OpenApiResponse(response=UserSerializer, description="ユーザー登録成功"),
        400: OpenApiResponse(description="バリデーションエラー"),
    },
)
class UserRegisterView(APIView):
    """
    新規ユーザー登録用ビュー。
    """

    permission_classes = [AllowAny]

    def post(self, request, format=None):
        ser = RegisterUserSerializer(data=request.data)
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


@extend_schema(
    summary="ユーザー一覧取得",
    tags=["ユーザー管理"],
    responses={
        200: OpenApiResponse(
            response=UserSerializer(many=True), description="ユーザー一覧"
        )
    },
)
class UserListView(APIView):
    """
    登録されているユーザーの一覧を取得するビュー。
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        users = User.objects.all()
        ser = UserSerializer(users, many=True)
        return api_response(data=ser.data, message="ユーザー一覧取得成功")


@extend_schema(
    summary="ユーザー詳細取得・更新・削除",
    tags=["ユーザー管理"],
    responses={
        200: OpenApiResponse(
            response=UserSerializer, description="ユーザー詳細取得成功"
        ),
        404: OpenApiResponse(description="該当ユーザーが存在しない"),
    },
)
class UserDetailView(APIView):
    """
    特定ユーザーの詳細情報取得・更新・削除を担当するビュー。
    """

    permission_classes = [IsAuthenticated]

    def get_object(self, id):
        """IDに基づき対象ユーザーを取得"""
        return get_object_or_404(User, id=id)

    def get(self, request, id):
        """ユーザー詳細情報取得"""
        user = self.get_object(id)
        ser = UserSerializer(user)
        return api_response(data=ser.data, message="ユーザー詳細取得成功")

    def put(self, request, id):
        """ユーザー情報更新"""
        user = self.get_object(id)
        ser = UserSerializer(user, data=request.data, partial=True)
        if ser.is_valid():
            ser.save()
            return api_response(data=ser.data, message="ユーザー更新成功")
        return api_response(
            message="更新失敗",
            data=ser.errors,
            code=400,
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, id):
        """ユーザー削除"""
        user = self.get_object(id)
        user.delete()
        return api_response(
            message="ユーザー削除成功", code=204, status_code=status.HTTP_204_NO_CONTENT
        )


@extend_schema(
    summary="JWTログイン",
    description="ユーザー名とパスワードを用いてアクセストークンとリフレッシュトークンを取得します。",
    tags=["認証"],
    responses={
        200: OpenApiResponse(description="ログイン成功"),
        401: OpenApiResponse(description="認証失敗"),
    },
)
class CustomTokenObtainPairView(TokenObtainPairView):
    """
    JWTによる認証（ログイン）用ビュー。
    """

    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]

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


@extend_schema(
    summary="アクセストークン更新",
    description="リフレッシュトークンを用いて新しいアクセストークンを取得するAPI。",
    tags=["認証"],
    responses={
        200: OpenApiResponse(response={"access": "新しいアクセストークン"}),
        401: OpenApiResponse(description="トークンが無効です"),
    },
)
class CustomTokenRefreshView(APIView):
    """
    アクセストークンをリフレッシュするビュー。
    """

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
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

        return api_response(
            data=serializer.validated_data, message="アクセストークン更新成功"
        )
