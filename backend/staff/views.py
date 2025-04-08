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


@api_view(["POST"])
def assign_night_shift(request):
    """
    夜勤を指定されたら、翌日を「明」、翌々日を「休」として自動的に登録。
    POST body:
    {
        "staff_id": 1,
        "night_date": "2024-04-01"
    }
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


@extend_schema(summary="職種一覧取得", tags=["スタッフ管理"])
class RoleListCreateView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        roles = Role.objects.all()
        serializer = RoleSerializer(roles, many=True)
        return api_response(data=serializer.data)

    def post(self, request):
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


@extend_schema(summary="職種詳細取得・更新・削除", tags=["スタッフ管理"])
class RoleDetailView(APIView):
    permission_classes = [IsAdminUser]

    def get_object(self, pk):
        return get_object_or_404(Role, pk=pk)

    def get(self, request, pk):
        role = self.get_object(pk)
        serializer = RoleSerializer(role)
        return api_response(data=serializer.data)

    def put(self, request, pk):
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

    def delete(self, request, pk):
        role = self.get_object(pk)
        role.delete()
        return api_response(
            message="職種を削除しました。",
            code=204,
            status_code=status.HTTP_204_NO_CONTENT,
        )


@extend_schema(summary="シフト種類一覧取得", tags=["スタッフ管理"])
class ShiftTypeListCreateView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        shifts = ShiftType.objects.all()
        serializer = ShiftTypeSerializer(shifts, many=True)
        return api_response(data=serializer.data)

    def post(self, request):
        serializer = ShiftTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(
                code=201,
                status_code=status.HTTP_201_CREATED,
                message="シフト種類を登録しました。",
                data=serializer.data,
            )
        return api_response(
            code=400,
            status_code=status.HTTP_400_BAD_REQUEST,
            message="バリデーションエラー",
            data=serializer.errors,
        )


@extend_schema(summary="シフト種類詳細取得・更新・削除", tags=["スタッフ管理"])
class ShiftTypeDetailView(APIView):
    permission_classes = [IsAdminUser]

    def get_object(self, pk):
        return get_object_or_404(ShiftType, pk=pk)

    def get(self, request, pk):
        shift = self.get_object(pk)
        serializer = ShiftTypeSerializer(shift)
        return api_response(data=serializer.data)

    def put(self, request, pk):
        shift = self.get_object(pk)
        serializer = ShiftTypeSerializer(shift, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(
                message="シフト種類を更新しました。", data=serializer.data
            )
        return api_response(
            code=400,
            status_code=status.HTTP_400_BAD_REQUEST,
            message="バリデーションエラー",
            data=serializer.errors,
        )

    def delete(self, request, pk):
        shift = self.get_object(pk)
        shift.delete()
        return api_response(
            message="シフト種類を削除しました。",
            code=204,
            status_code=status.HTTP_204_NO_CONTENT,
        )


@extend_schema(
    summary="スタッフ一覧取得",
    tags=["スタッフ管理"],
    responses={200: StaffSerializer(many=True)},
)
class StaffListCreateView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        staffs = Staff.objects.all()
        serializer = StaffSerializer(staffs, many=True)
        return api_response(data=serializer.data)

    def post(self, request):
        serializer = StaffSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(
                code=201,
                status_code=status.HTTP_201_CREATED,
                message="スタッフを登録しました。",
                data=serializer.data,
            )
        return api_response(
            code=400,
            status_code=status.HTTP_400_BAD_REQUEST,
            message="バリデーションエラー",
            data=serializer.errors,
        )


@extend_schema(
    summary="スタッフ詳細取得・更新・削除",
    tags=["スタッフ管理"],
    responses={200: StaffSerializer},
)
class StaffDetailView(APIView):
    permission_classes = [IsAdminUser]

    def get_object(self, pk):
        return get_object_or_404(Staff, pk=pk)

    def get(self, request, pk):
        staff = self.get_object(pk)
        serializer = StaffSerializer(staff)
        return api_response(data=serializer.data)

    def put(self, request, pk):
        staff = self.get_object(pk)
        serializer = StaffSerializer(staff, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(
                message="スタッフ情報を更新しました。", data=serializer.data
            )
        return api_response(
            code=400,
            status_code=status.HTTP_400_BAD_REQUEST,
            message="バリデーションエラー",
            data=serializer.errors,
        )

    def delete(self, request, pk):
        staff = self.get_object(pk)
        staff.delete()
        return api_response(
            message="スタッフを削除しました。",
            code=204,
            status_code=status.HTTP_204_NO_CONTENT,
        )


@extend_schema(summary="勤務シフト一覧取得・登録", tags=["スタッフ管理"])
class WorkScheduleListCreateView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        schedules = WorkSchedule.objects.all()
        serializer = WorkScheduleSerializer(schedules, many=True)
        return api_response(data=serializer.data)

    def post(self, request):
        serializer = WorkScheduleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(
                code=201,
                status_code=status.HTTP_201_CREATED,
                message="勤務シフトを登録しました。",
                data=serializer.data,
            )
        return api_response(
            code=400,
            status_code=status.HTTP_400_BAD_REQUEST,
            message="バリデーションエラー",
            data=serializer.errors,
        )


@extend_schema(summary="勤務シフト詳細取得・更新・削除", tags=["スタッフ管理"])
class WorkScheduleDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        return get_object_or_404(WorkSchedule, pk=pk)

    def get(self, request, pk):
        schedule = self.get_object(pk)
        serializer = WorkScheduleSerializer(schedule)
        return api_response(data=serializer.data)

    def put(self, request, pk):
        schedule = self.get_object(pk)
        serializer = WorkScheduleSerializer(schedule, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(
                message="勤務シフトを更新しました。", data=serializer.data
            )
        return api_response(
            code=400,
            status_code=status.HTTP_400_BAD_REQUEST,
            message="バリデーションエラー",
            data=serializer.errors,
        )

    def delete(self, request, pk):
        schedule = self.get_object(pk)
        schedule.delete()
        return api_response(
            message="勤務シフトを削除しました。",
            code=204,
            status_code=status.HTTP_204_NO_CONTENT,
        )
