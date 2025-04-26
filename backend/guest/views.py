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

# ------------------------- 利用者管理 -------------------------


class GuestListCreateView(APIView):
    """
    利用者の一覧取得・新規登録を行うAPIビュー
    """

    permission_classes = [IsAdminUser]

    @extend_schema(
        operation_id="GuestList",
        summary="利用者一覧の取得",
        description="すべての利用者情報を一覧で取得します。",
        tags=["利用者管理"],
    )
    def get(self, request):
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests, many=True)
        return api_response(data=serializer.data)

    @extend_schema(
        operation_id="GuestCreate",
        summary="利用者の新規登録",
        description="新しい利用者を登録します。",
        tags=["利用者管理"],
    )
    def post(self, request):
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(
                data=serializer.data, message="登録成功", code=status.HTTP_201_CREATED
            )
        return api_response(
            code=status.HTTP_400_BAD_REQUEST, message="登録失敗", data=serializer.errors
        )


class GuestDetailView(APIView):
    """
    利用者の詳細取得・更新・削除を行うAPIビュー
    """

    permission_classes = [IsAdminUser]

    def get_object(self, pk):
        return Guest.objects.get(pk=pk)

    @extend_schema(
        operation_id="GuestRetrieve",
        summary="利用者の詳細取得",
        description="特定の利用者情報を取得します。",
        tags=["利用者管理"],
    )
    def get(self, request, pk):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest)
        return api_response(data=serializer.data)

    @extend_schema(
        operation_id="GuestUpdate",
        summary="利用者情報の更新",
        description="特定の利用者情報を更新します。",
        tags=["利用者管理"],
    )
    def put(self, request, pk):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(data=serializer.data, message="更新成功")
        return api_response(
            code=status.HTTP_400_BAD_REQUEST, message="更新失敗", data=serializer.errors
        )

    @extend_schema(
        operation_id="GuestDelete",
        summary="利用者の削除",
        description="特定の利用者情報を削除します。",
        tags=["利用者管理"],
    )
    def delete(self, request, pk):
        guest = self.get_object(pk)
        guest.delete()
        return api_response(message="削除成功", code=status.HTTP_204_NO_CONTENT)


# ------------------------- 来訪種別管理 -------------------------


class VisitTypeListCreateView(APIView):
    """
    来訪種別（泊まり、通い、休みなど）の一覧取得・新規登録APIビュー
    """

    permission_classes = [IsAdminUser]

    @extend_schema(
        operation_id="VisitTypeList",
        summary="来訪種別一覧の取得",
        description="登録済みの来訪種別（泊まり、通い、休み等）の一覧を取得します。",
        tags=["利用者管理"],
    )
    def get(self, request):
        types = VisitType.objects.all()
        serializer = VisitTypeSerializer(types, many=True)
        return api_response(data=serializer.data)

    @extend_schema(
        operation_id="VisitTypeCreate",
        summary="来訪種別の新規登録",
        description="新しい来訪種別を登録します。",
        tags=["利用者管理"],
    )
    def post(self, request):
        serializer = VisitTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(
                data=serializer.data, message="登録成功", code=status.HTTP_201_CREATED
            )
        return api_response(
            code=status.HTTP_400_BAD_REQUEST, message="登録失敗", data=serializer.errors
        )


class VisitTypeDetailView(APIView):
    """
    来訪種別の詳細取得・更新・削除APIビュー
    """

    permission_classes = [IsAdminUser]

    def get_object(self, pk):
        return VisitType.objects.get(pk=pk)

    @extend_schema(
        operation_id="VisitTypeRetrieve",
        summary="来訪種別の詳細取得",
        description="特定の来訪種別情報を取得します。",
        tags=["利用者管理"],
    )
    def get(self, request, pk):
        obj = self.get_object(pk)
        serializer = VisitTypeSerializer(obj)
        return api_response(data=serializer.data)

    @extend_schema(
        operation_id="VisitTypeUpdate",
        summary="来訪種別の更新",
        description="特定の来訪種別情報を更新します。",
        tags=["利用者管理"],
    )
    def put(self, request, pk):
        obj = self.get_object(pk)
        serializer = VisitTypeSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(data=serializer.data, message="更新成功")
        return api_response(
            code=status.HTTP_400_BAD_REQUEST, message="更新失敗", data=serializer.errors
        )

    @extend_schema(
        operation_id="VisitTypeDelete",
        summary="来訪種別の削除",
        description="特定の来訪種別情報を削除します。",
        tags=["利用者管理"],
    )
    def delete(self, request, pk):
        obj = self.get_object(pk)
        obj.delete()
        return api_response(message="削除成功", code=status.HTTP_204_NO_CONTENT)


# ------------------------- スケジュール管理 -------------------------


class VisitScheduleListCreateView(APIView):
    """
    来訪スケジュール一覧取得・新規登録APIビュー
    """

    permission_classes = [IsAuthenticatedOrReadOnly]

    @extend_schema(
        operation_id="VisitScheduleList",
        summary="スケジュール一覧の取得",
        description="すべての来訪スケジュールを一覧で取得します。",
        tags=["利用者管理"],
    )
    def get(self, request):
        qs = VisitSchedule.objects.all()
        serializer = VisitScheduleSerializer(qs, many=True)
        return api_response(data=serializer.data)

    @extend_schema(
        operation_id="VisitScheduleCreate",
        summary="スケジュールの新規登録",
        description="新しい来訪スケジュールを登録します。",
        tags=["利用者管理"],
    )
    def post(self, request):
        serializer = VisitScheduleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(
                data=serializer.data, message="登録成功", code=status.HTTP_201_CREATED
            )
        return api_response(
            code=status.HTTP_400_BAD_REQUEST, message="登録失敗", data=serializer.errors
        )


class VisitScheduleDetailView(APIView):
    """
    来訪スケジュール詳細取得・更新・削除APIビュー
    """

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        return VisitSchedule.objects.get(pk=pk)

    @extend_schema(
        operation_id="VisitScheduleRetrieve",
        summary="スケジュールの詳細取得",
        description="特定の来訪スケジュール情報を取得します。",
        tags=["利用者管理"],
    )
    def get(self, request, pk):
        obj = self.get_object(pk)
        serializer = VisitScheduleSerializer(obj)
        return api_response(data=serializer.data)

    @extend_schema(
        operation_id="VisitScheduleUpdate",
        summary="スケジュールの更新",
        description="特定の来訪スケジュール情報を更新します。",
        tags=["利用者管理"],
    )
    def put(self, request, pk):
        obj = self.get_object(pk)
        serializer = VisitScheduleSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(data=serializer.data, message="更新成功")
        return api_response(
            code=status.HTTP_400_BAD_REQUEST, message="更新失敗", data=serializer.errors
        )

    @extend_schema(
        operation_id="VisitScheduleDelete",
        summary="スケジュールの削除",
        description="特定の来訪スケジュール情報を削除します。",
        tags=["利用者管理"],
    )
    def delete(self, request, pk):
        obj = self.get_object(pk)
        obj.delete()
        return api_response(message="削除成功", code=status.HTTP_204_NO_CONTENT)


class ScheduleUploadView(APIView):
    """
    OCR画像からスケジュール登録APIビュー
    """

    permission_classes = [IsAdminUser]

    @extend_schema(
        operation_id="ScheduleUpload",
        summary="画像からスケジュール登録",
        description="画像ファイルをOCR解析し、来訪スケジュールを自動登録します。",
        tags=["利用者管理"],
    )
    def post(self, request, *args, **kwargs):
        serializer = ScheduleUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return api_response(
                code=status.HTTP_400_BAD_REQUEST,
                message="画像ファイルが無効です。",
                data=serializer.errors,
            )

        image_file = serializer.validated_data["image"]

        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            temp_file.write(image_file.read())
            temp_path = temp_file.name

        processor = ScheduleOCRProcessor(temp_path)
        result = processor.run()

        return api_response(
            message=f"{result['count']}件の訪問スケジュールを保存しました。",
            data={
                "guest": result["guest"],
                "year": result["year"],
                "month": result["month"],
            },
        )
