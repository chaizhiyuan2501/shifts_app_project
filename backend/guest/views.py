from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from drf_spectacular.utils import extend_schema

import tempfile
from utils.api_response_utils import api_response
from guest.utils.ocr_utils import ScheduleOCRProcessor

from .models import Guest, VisitType, VisitSchedule
from .serializers import (
    GuestSerializer,
    VisitTypeSerializer,
    VisitScheduleSerializer,
    ScheduleUploadSerializer,
)


# ========================================
# 利用者（Guest）API
# ========================================

class GuestListCreateView(APIView):
    """
    利用者の一覧取得と新規登録を行うAPIビュー
    """
    permission_classes = [IsAdminUser]

    @extend_schema(summary="利用者一覧の取得", tags=["利用者管理"])
    def get(self, request):
        """
        全利用者を取得する（管理者のみ）
        """
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests, many=True)
        return api_response(data=serializer.data)

    @extend_schema(summary="利用者の新規登録", tags=["利用者管理"])
    def post(self, request):
        """
        新しい利用者を登録する（管理者のみ）
        """
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(data=serializer.data, message="登録成功", code=status.HTTP_201_CREATED)
        return api_response(code=status.HTTP_400_BAD_REQUEST, message="登録失敗", data=serializer.errors)


class GuestDetailView(APIView):
    """
    利用者の詳細取得・更新・削除を行うAPIビュー
    """
    permission_classes = [IsAdminUser]

    def get_object(self, pk):
        return Guest.objects.get(pk=pk)

    @extend_schema(summary="利用者の詳細取得", tags=["利用者管理"])
    def get(self, request, pk):
        """
        指定された利用者の詳細を取得する
        """
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest)
        return api_response(data=serializer.data)

    @extend_schema(summary="利用者情報の更新", tags=["利用者管理"])
    def put(self, request, pk):
        """
        指定された利用者の情報を更新する
        """
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(data=serializer.data, message="更新成功")
        return api_response(code=status.HTTP_400_BAD_REQUEST, message="更新失敗", data=serializer.errors)

    @extend_schema(summary="利用者の削除", tags=["利用者管理"])
    def delete(self, request, pk):
        """
        指定された利用者を削除する
        """
        guest = self.get_object(pk)
        guest.delete()
        return api_response(message="削除成功", code=status.HTTP_204_NO_CONTENT)


# ========================================
# 来訪種別（VisitType）API
# ========================================

class VisitTypeListCreateView(APIView):
    """
    来訪種別（泊まり、通い、休みなど）の一覧取得・新規登録用APIビュー
    """
    permission_classes = [IsAdminUser]

    @extend_schema(summary="来訪種別一覧の取得", tags=["利用者管理"])
    def get(self, request):
        """
        来訪種別の一覧を取得する
        """
        types = VisitType.objects.all()
        serializer = VisitTypeSerializer(types, many=True)
        return api_response(data=serializer.data)

    @extend_schema(summary="来訪種別の新規登録", tags=["利用者管理"])
    def post(self, request):
        """
        来訪種別を新規登録する
        """
        serializer = VisitTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(data=serializer.data, message="登録成功", code=status.HTTP_201_CREATED)
        return api_response(code=status.HTTP_400_BAD_REQUEST, message="登録失敗", data=serializer.errors)


class VisitTypeDetailView(APIView):
    """
    来訪種別の詳細取得・更新・削除を行うAPIビュー
    """
    permission_classes = [IsAdminUser]

    def get_object(self, pk):
        return VisitType.objects.get(pk=pk)

    @extend_schema(summary="来訪種別の詳細取得", tags=["利用者管理"])
    def get(self, request, pk):
        """
        指定された来訪種別の情報を取得する
        """
        obj = self.get_object(pk)
        serializer = VisitTypeSerializer(obj)
        return api_response(data=serializer.data)

    @extend_schema(summary="来訪種別の更新", tags=["利用者管理"])
    def put(self, request, pk):
        """
        指定された来訪種別を更新する
        """
        obj = self.get_object(pk)
        serializer = VisitTypeSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(data=serializer.data, message="更新成功")
        return api_response(code=status.HTTP_400_BAD_REQUEST, message="更新失敗", data=serializer.errors)

    @extend_schema(summary="来訪種別の削除", tags=["利用者管理"])
    def delete(self, request, pk):
        """
        指定された来訪種別を削除する
        """
        obj = self.get_object(pk)
        obj.delete()
        return api_response(message="削除成功", code=status.HTTP_204_NO_CONTENT)


# ========================================
# スケジュール（VisitSchedule）API
# ========================================

class VisitScheduleListCreateView(APIView):
    """
    利用者の来訪スケジュール一覧取得・登録用APIビュー
    """
    permission_classes = [IsAuthenticatedOrReadOnly]

    @extend_schema(summary="スケジュール一覧の取得", tags=["利用者管理"])
    def get(self, request):
        """
        全スケジュールの一覧を取得する
        """
        qs = VisitSchedule.objects.all()
        serializer = VisitScheduleSerializer(qs, many=True)
        return api_response(data=serializer.data)

    @extend_schema(summary="スケジュールの新規登録", tags=["利用者管理"])
    def post(self, request):
        """
        新しいスケジュールを登録する
        """
        serializer = VisitScheduleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(data=serializer.data, message="登録成功", code=status.HTTP_201_CREATED)
        return api_response(code=status.HTTP_400_BAD_REQUEST, message="登録失敗", data=serializer.errors)


class VisitScheduleDetailView(APIView):
    """
    スケジュールの詳細取得・更新・削除を行うAPIビュー
    """
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        return VisitSchedule.objects.get(pk=pk)

    @extend_schema(summary="スケジュールの詳細取得", tags=["利用者管理"])
    def get(self, request, pk):
        """
        指定されたスケジュールを取得する
        """
        obj = self.get_object(pk)
        serializer = VisitScheduleSerializer(obj)
        return api_response(data=serializer.data)

    @extend_schema(summary="スケジュールの更新", tags=["利用者管理"])
    def put(self, request, pk):
        """
        指定されたスケジュールを更新する
        """
        obj = self.get_object(pk)
        serializer = VisitScheduleSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(data=serializer.data, message="更新成功")
        return api_response(code=status.HTTP_400_BAD_REQUEST, message="更新失敗", data=serializer.errors)

    @extend_schema(summary="スケジュールの削除", tags=["利用者管理"])
    def delete(self, request, pk):
        """
        指定されたスケジュールを削除する
        """
        obj = self.get_object(pk)
        obj.delete()
        return api_response(message="削除成功", code=status.HTTP_204_NO_CONTENT)


# ========================================
# OCRによるスケジュール画像解析
# ========================================

@extend_schema(
    summary="画像からスケジュールを登録する",
    description="画像からAI-OCRによりスケジュール情報を抽出し、自動でDBに保存します。",
    tags=["利用者管理"],
)
class ScheduleUploadView(APIView):
    """
    OCRで解析した画像からスケジュールを自動登録するAPI
    """
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        """
        画像をアップロードしてOCR処理を実行する
        """
        serializer = ScheduleUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return api_response(
                code=status.HTTP_400_BAD_REQUEST,
                message="画像ファイルが無効です。",
                data=serializer.errors
            )

        image_file = serializer.validated_data["image"]

        # 一時ファイルに保存（PILとOpenCV両方対応のため）
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            temp_file.write(image_file.read())
            temp_path = temp_file.name

        # OCR処理とDB登録
        processor = ScheduleOCRProcessor(temp_path)
        result = processor.run()

        return api_response(
            message=f"{result['count']}件の訪問スケジュールを保存しました。",
            data={
                "guest": result["guest"],
                "year": result["year"],
                "month": result["month"],
            }
        )
