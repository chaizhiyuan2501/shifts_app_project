from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)
from drf_spectacular.utils import extend_schema
from datetime import timedelta, datetime
from .models import Role, Staff, ShiftType, WorkSchedule
from django.contrib.auth.models import User

from .serializers import (
    RoleSerializer,
    StaffSerializer,
    ShiftTypeSerializer,
    WorkScheduleSerializer,
)


@extend_schema(
    summary="夜勤シフトの自動登録",
    description="夜勤を登録した際に、翌日を『明け』、翌々日を『休み』として自動的にシフトを登録します。",
    methods=["POST"],
    request={
        "application/json": {"example": {"staff_id": 1, "night_date": "2024-04-01"}}
    },
    responses={
        201: {
            "example": {
                "message": "夜勤＋明け＋休みのスケジュールを登録しました。",
                "schedule": [
                    {"date": "2024-04-01", "shift": "夜", "created": True},
                    {"date": "2024-04-02", "shift": "明", "created": True},
                    {"date": "2024-04-03", "shift": "休", "created": True},
                ],
            }
        }
    },
)
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


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAdminUser]


class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = [IsAdminUser]


class ShiftTypeViewSet(viewsets.ModelViewSet):
    queryset = ShiftType.objects.all()
    serializer_class = ShiftTypeSerializer
    permission_classes = [IsAdminUser]


class WorkScheduleViewSet(viewsets.ModelViewSet):
    queryset = WorkSchedule.objects.all()
    serializer_class = WorkScheduleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
