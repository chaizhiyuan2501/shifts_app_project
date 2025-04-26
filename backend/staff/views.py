from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import timedelta, datetime
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from drf_spectacular.utils import extend_schema, OpenApiResponse

from .models import ShiftType, Staff, Role, WorkSchedule
from .serializers import (
    ShiftTypeSerializer,
    StaffSerializer,
    RoleSerializer,
    WorkScheduleSerializer,
)
from utils.api_response_utils import api_response


# 夜勤シフトの自動割り当てAPI
@extend_schema(
    operation_id="AssignNightShift",
    summary="夜勤シフトの自動割り当て",
    description="指定されたスタッフに対し、夜勤・明け・休みシフトを連続登録します。",
    tags=["スタッフ管理"],
    responses={
        201: OpenApiResponse(description="夜勤シフト作成成功"),
        400: OpenApiResponse(description="リクエストエラー"),
    },
)
@api_view(["POST"])
def assign_night_shift(request):
    """
    指定スタッフに夜勤、明け、休みのシフトを3日連続で登録するAPI。
    """
    try:
        staff = Staff.objects.get(pk=request.data["staff_id"])
        night_date = datetime.strptime(request.data["night_date"], "%Y-%m-%d").date()
    except (KeyError, ValueError, Staff.DoesNotExist):
        return Response(
            {"error": "データが不正です"}, status=status.HTTP_400_BAD_REQUEST
        )

    shift_night = ShiftType.objects.get(code="夜")
    shift_after = ShiftType.objects.get(code="明")
    shift_rest = ShiftType.objects.get(code="休")

    results = []

    for offset, shift in zip(range(3), [shift_night, shift_after, shift_rest]):
        target_date = night_date + timedelta(days=offset)
        obj, created = WorkSchedule.objects.update_or_create(
            staff=staff, date=target_date, defaults={"shift": shift}
        )
        results.append({"date": target_date, "shift": shift.code, "created": created})

    return Response(
        {
            "message": "夜勤シフトおよび翌日・翌々日のシフトを登録しました。",
            "schedule": results,
        },
        status=status.HTTP_201_CREATED,
    )


# ===== Role モデル用のCRUD API =====


class RoleListCreateView(APIView):
    permission_classes = [IsAdminUser]

    @extend_schema(
        operation_id="RoleList",
        summary="職種一覧取得",
        tags=["スタッフ管理"],
        responses={200: OpenApiResponse(description="職種一覧取得成功")},
    )
    def get(self, request):
        """
        職種(Role)の一覧を取得するAPI。
        """
        roles = Role.objects.all()
        serializer = RoleSerializer(roles, many=True)
        return api_response(data=serializer.data)

    @extend_schema(
        operation_id="RoleCreate",
        summary="職種新規登録",
        tags=["スタッフ管理"],
        request=RoleSerializer,
        responses={
            201: OpenApiResponse(description="職種作成成功"),
            400: OpenApiResponse(description="バリデーションエラー"),
        },
    )
    def post(self, request):
        """
        新しい職種(Role)を登録するAPI。
        """
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(
                code=201,
                status_code=status.HTTP_201_CREATED,
                message="職種を登録しました。",
                data=serializer.data,
            )
        return api_response(
            code=400,
            status_code=status.HTTP_400_BAD_REQUEST,
            message="バリデーションエラー",
            data=serializer.errors,
        )


class RoleDetailView(APIView):
    permission_classes = [IsAdminUser]

    def get_object(self, pk):
        """
        指定したIDの職種(Role)オブジェクトを取得する内部メソッド。
        """
        return get_object_or_404(Role, pk=pk)

    @extend_schema(
        operation_id="RoleRetrieve",
        summary="職種詳細取得",
        tags=["スタッフ管理"],
        responses={
            200: OpenApiResponse(description="職種詳細取得成功"),
            404: OpenApiResponse(description="該当職種が存在しない"),
        },
    )
    def get(self, request, pk):
        """
        特定の職種(Role)の詳細情報を取得するAPI。
        """
        role = self.get_object(pk)
        serializer = RoleSerializer(role)
        return api_response(data=serializer.data)

    @extend_schema(
        operation_id="RoleUpdate",
        summary="職種情報更新",
        tags=["スタッフ管理"],
        request=RoleSerializer,
        responses={
            200: OpenApiResponse(description="職種更新成功"),
            400: OpenApiResponse(description="バリデーションエラー"),
        },
    )
    def put(self, request, pk):
        """
        特定の職種(Role)情報を更新するAPI。
        """
        role = self.get_object(pk)
        serializer = RoleSerializer(role, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(
                message="職種情報を更新しました。", data=serializer.data
            )
        return api_response(
            code=400,
            status_code=status.HTTP_400_BAD_REQUEST,
            message="バリデーションエラー",
            data=serializer.errors,
        )

    @extend_schema(
        operation_id="RoleDelete",
        summary="職種削除",
        tags=["スタッフ管理"],
        responses={
            204: OpenApiResponse(description="職種削除成功"),
            404: OpenApiResponse(description="該当職種が存在しない"),
        },
    )
    def delete(self, request, pk):
        """
        特定の職種(Role)を削除するAPI。
        """
        role = self.get_object(pk)
        role.delete()
        return api_response(
            message="職種を削除しました。",
            code=204,
            status_code=status.HTTP_204_NO_CONTENT,
        )
