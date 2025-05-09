from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiResponse

from .models import ShiftType, Staff, Role, WorkSchedule
from .serializers import (
    ShiftTypeSerializer,
    StaffSerializer,
    RoleSerializer,
    WorkScheduleSerializer,
)
from utils.api_response_utils import api_response
from staff.utils.shift_utils import assign_night_shift


# ================================================================
# Role（職種）CRUD
# ================================================================
class RoleListCreateView(APIView):
    """職種一覧取得・新規登録"""

    permission_classes = [IsAdminUser]
    model = Role
    serializer_class = RoleSerializer

    @extend_schema(
        operation_id="RoleList",
        summary="職種一覧取得",
        tags=["スタッフ管理"],
        responses={200: OpenApiResponse(description="職種一覧取得成功")},
    )
    def get(self, request):
        roles = self.model.objects.all()
        ser = self.serializer_class(roles, many=True)
        return api_response(data=ser.data)

    @extend_schema(
        operation_id="RoleCreate",
        summary="職種新規登録",
        tags=["スタッフ管理"],
        request=RoleSerializer,  # 登録に必要な項目を前端に示す
        responses={
            201: OpenApiResponse(description="職種作成成功"),
            400: OpenApiResponse(description="バリデーションエラー"),
        },
    )
    def post(self, request):
        ser = self.serializer_class(data=request.data)
        if ser.is_valid():
            ser.save()
            return api_response(code=201, message="職種を登録しました。", data=ser.data)
        return api_response(code=400, message="バリデーションエラー", data=ser.errors)


class RoleDetailView(APIView):
    """職種詳細・更新・削除"""

    permission_classes = [IsAdminUser]
    model = Role
    serializer_class = RoleSerializer

    def get_object(self, pk):
        """存在チェックを含む取得ヘルパー"""
        return get_object_or_404(self.model, pk=pk)

    @extend_schema(
        operation_id="RoleRetrieve",
        summary="職種詳細取得",
        tags=["スタッフ管理"],
        responses={
            200: OpenApiResponse(description="取得成功"),
            404: OpenApiResponse(description="存在しない"),
        },
    )
    def get(self, request, pk):
        ser = self.serializer_class(self.get_object(pk))
        return api_response(data=ser.data)

    @extend_schema(
        operation_id="RoleUpdate",
        summary="職種更新",
        tags=["スタッフ管理"],
        request=RoleSerializer,
        responses={
            200: OpenApiResponse(description="更新成功"),
            400: OpenApiResponse(description="バリデーションエラー"),
        },
    )
    def put(self, request, pk):
        role = self.get_object(pk)
        ser = self.serializer_class(role, data=request.data)
        if ser.is_valid():
            ser.save()
            return api_response(message="更新成功", data=ser.data)
        return api_response(code=400, message="バリデーションエラー", data=ser.errors)

    @extend_schema(
        operation_id="RoleDelete",
        summary="職種削除",
        tags=["スタッフ管理"],
        responses={
            204: OpenApiResponse(description="削除成功"),
            404: OpenApiResponse(description="存在しない"),
        },
    )
    def delete(self, request, pk):
        self.get_object(pk).delete()
        return api_response(message="削除成功", code=204)


# ================================================================
# ShiftType（シフト種類）CRUD
# ================================================================
class ShiftTypeListCreateView(APIView):
    """シフト種類一覧・新規登録"""

    permission_classes = [IsAdminUser]
    model = ShiftType
    serializer_class = ShiftTypeSerializer

    @extend_schema(
        operation_id="ShiftTypeList",
        summary="シフト種類一覧取得",
        tags=["スタッフ管理"],
        responses={200: OpenApiResponse(description="一覧取得成功")},
    )
    def get(self, request):
        ser = self.serializer_class(self.model.objects.all(), many=True)
        return api_response(data=ser.data)

    @extend_schema(
        operation_id="ShiftTypeCreate",
        summary="シフト種類新規登録",
        tags=["スタッフ管理"],
        request=ShiftTypeSerializer,
        responses={
            201: OpenApiResponse(description="シフト種類を登録しました。"),
            400: OpenApiResponse(description="バリデーションエラー"),
        },
    )
    def post(self, request):
        ser = self.serializer_class(data=request.data)
        if ser.is_valid():
            ser.save()
            return api_response(
                code=201, message="シフト種類を登録しました。", data=ser.data
            )
        return api_response(code=400, message="バリデーションエラー", data=ser.errors)


class ShiftTypeDetailView(APIView):
    """シフト種類詳細・更新・削除"""

    permission_classes = [IsAdminUser]
    model = ShiftType
    serializer_class = ShiftTypeSerializer

    def get_object(self, pk):
        return get_object_or_404(self.model, pk=pk)

    @extend_schema(
        operation_id="ShiftTypeRetrieve",
        summary="シフト種類詳細取得",
        tags=["スタッフ管理"],
        responses={
            200: OpenApiResponse(description="取得成功"),
            404: OpenApiResponse(description="存在しない"),
        },
    )
    def get(self, request, pk):
        ser = self.serializer_class(self.get_object(pk))
        return api_response(data=ser.data)

    @extend_schema(
        operation_id="ShiftTypeUpdate",
        summary="シフト種類更新",
        tags=["スタッフ管理"],
        request=ShiftTypeSerializer,
        responses={
            200: OpenApiResponse(description="更新成功"),
            400: OpenApiResponse(description="バリデーションエラー"),
        },
    )
    def put(self, request, pk):
        shift = self.get_object(pk)
        ser = self.serializer_class(shift, data=request.data)
        if ser.is_valid():
            ser.save()
            return api_response(message="更新成功", data=ser.data)
        return api_response(code=400, message="バリデーションエラー", data=ser.errors)

    @extend_schema(
        operation_id="ShiftTypeDelete",
        summary="シフト種類削除",
        tags=["スタッフ管理"],
        responses={
            204: OpenApiResponse(description="削除成功"),
            404: OpenApiResponse(description="存在しない"),
        },
    )
    def delete(self, request, pk):
        self.get_object(pk).delete()
        return api_response(message="削除成功", code=204)


# ================================================================
# Staff CRUD
# ================================================================
class StaffListCreateView(APIView):
    """スタッフ一覧・新規登録"""

    permission_classes = [IsAdminUser]
    model = Staff
    serializer_class = StaffSerializer

    @extend_schema(
        operation_id="StaffList",
        summary="スタッフ一覧取得",
        tags=["スタッフ管理"],
        responses={200: OpenApiResponse(description="一覧取得成功")},
    )
    def get(self, request):
        ser = self.serializer_class(self.model.objects.all(), many=True)
        return api_response(data=ser.data)

    @extend_schema(
        operation_id="StaffCreate",
        summary="スタッフ新規登録",
        tags=["スタッフ管理"],
        request=StaffSerializer,
        responses={
            201: OpenApiResponse(description="作成成功"),
            400: OpenApiResponse(description="バリデーションエラー"),
        },
    )
    def post(self, request):
        ser = self.serializer_class(data=request.data, context={"request": request})
        if ser.is_valid():
            ser.save()
            return api_response(code=201, message="登録成功", data=ser.data)
        return api_response(code=400, message="バリデーションエラー", data=ser.errors)


class StaffDetailView(APIView):
    """スタッフ詳細・更新・削除"""

    permission_classes = [IsAdminUser]
    model = Staff
    serializer_class = StaffSerializer

    def get_object(self, pk):
        return get_object_or_404(self.model, pk=pk)

    @extend_schema(
        operation_id="StaffRetrieve",
        summary="スタッフ詳細取得",
        tags=["スタッフ管理"],
        responses={
            200: OpenApiResponse(description="取得成功"),
            404: OpenApiResponse(description="存在しない"),
        },
    )
    def get(self, request, pk):
        ser = self.serializer_class(self.get_object(pk))
        return api_response(data=ser.data)

    @extend_schema(
        operation_id="StaffUpdate",
        summary="スタッフ更新",
        tags=["スタッフ管理"],
        request=StaffSerializer,
        responses={
            200: OpenApiResponse(description="更新成功"),
            400: OpenApiResponse(description="バリデーションエラー"),
        },
    )
    def put(self, request, pk):
        staff = self.get_object(pk)
        ser = self.serializer_class(staff, data=request.data)
        if ser.is_valid():
            ser.save()
            return api_response(message="更新成功", data=ser.data)
        return api_response(code=400, message="バリデーションエラー", data=ser.errors)

    @extend_schema(
        operation_id="StaffDelete",
        summary="スタッフ削除",
        tags=["スタッフ管理"],
        responses={
            204: OpenApiResponse(description="削除成功"),
            404: OpenApiResponse(description="存在しない"),
        },
    )
    def delete(self, request, pk):
        self.get_object(pk).delete()
        return api_response(message="削除成功", code=204)


# ================================================================
# WorkSchedule CRUD
# ================================================================
class WorkScheduleListCreateView(APIView):
    """
    勤務シフト一覧・新規登録
    """

    permission_classes = [IsAuthenticatedOrReadOnly]
    model = WorkSchedule
    serializer_class = WorkScheduleSerializer

    @extend_schema(
        operation_id="WorkScheduleList",
        summary="勤務シフト一覧取得",
        tags=["スタッフ管理"],
        responses={200: OpenApiResponse(description="一覧取得成功")},
    )
    def get(self, request):
        ser = self.serializer_class(self.model.objects.all(), many=True)
        return api_response(data=ser.data)

    @extend_schema(
        operation_id="WorkScheduleCreate",
        summary="勤務シフト新規登録",
        tags=["スタッフ管理"],
        request=WorkScheduleSerializer,
        responses={
            201: OpenApiResponse(description="勤務シフトを登録しました。"),
            400: OpenApiResponse(description="バリデーションエラー"),
        },
    )
    def post(self, request):
        ser = self.serializer_class(data=request.data)
        if ser.is_valid():
            staff = ser.validated_data.get("staff")
            shift = ser.validated_data.get("shift")
            if shift.code == "夜":
                # 夜勤の場合：夜→明→休 を3日分登録
                results = assign_night_shift(
                    staff_id=staff.id,
                    base_date=ser.validated_data.get("date"),
                )
                return api_response(
                    code=201, message="夜勤シフト3日分を登録しました。", data=results
                )
            else:
                ser.save()
                return api_response(
                    code=201, message="勤務シフトを登録しました。", data=ser.data
                )
        return api_response(code=400, message="バリデーションエラー", data=ser.errors)


class WorkScheduleDetailView(APIView):
    """
    勤務シフト詳細・更新・削除
    """

    permission_classes = [IsAuthenticatedOrReadOnly]
    model = WorkSchedule
    serializer_class = WorkScheduleSerializer

    def get_object(self, pk):
        return get_object_or_404(self.model, pk=pk)

    @extend_schema(
        operation_id="WorkScheduleRetrieve",
        summary="勤務シフト詳細取得",
        tags=["スタッフ管理"],
        responses={
            200: OpenApiResponse(description="取得成功"),
            404: OpenApiResponse(description="存在しない"),
        },
    )
    def get(self, request, pk):
        ser = self.serializer_class(self.get_object(pk))
        return api_response(data=ser.data)

    @extend_schema(
        operation_id="WorkScheduleUpdate",
        summary="勤務シフト更新",
        tags=["スタッフ管理"],
        request=WorkScheduleSerializer,
        responses={
            200: OpenApiResponse(description="更新成功"),
            400: OpenApiResponse(description="バリデーションエラー"),
        },
    )
    def put(self, request, pk):
        schedule = self.get_object(pk)
        ser = self.serializer_class(schedule, data=request.data)
        if ser.is_valid():
            shift_id = ser.validated_data.get("shift_id")
            shift = ShiftType.objects.get(id=shift_id)
            if shift.code == "夜":
                results = assign_night_shift(
                    shift=ser.validated_data.get("shift"),
                    base_date=ser.validated_data.get("date"),
                )
                return api_response(
                    code=201, message="夜勤シフト3日分を登録しました。", data=results
                )
            else:
                ser.save()
                return api_response(message="更新成功", data=ser.data)
        return api_response(code=400, message="バリデーションエラー", data=ser.errors)

    @extend_schema(
        operation_id="WorkScheduleDelete",
        summary="勤務シフト削除",
        tags=["スタッフ管理"],
        responses={
            204: OpenApiResponse(description="削除成功"),
            404: OpenApiResponse(description="存在しない"),
        },
    )
    def delete(self, request, pk):
        self.get_object(pk).delete()
        return api_response(message="削除成功", code=204)
