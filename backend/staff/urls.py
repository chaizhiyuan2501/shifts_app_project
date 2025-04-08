from django.urls import path
from .views import (
    RoleListCreateView, RoleDetailView,
    ShiftTypeListCreateView, ShiftTypeDetailView,
    StaffListCreateView, StaffDetailView,
    WorkScheduleListCreateView, WorkScheduleDetailView,
    assign_night_shift,
)

urlpatterns = [
    # 職種
    path("roles/", RoleListCreateView.as_view(), name="role-list"),
    path("roles/<int:pk>/", RoleDetailView.as_view(), name="role-detail"),

    # シフト種類
    path("shift-types/", ShiftTypeListCreateView.as_view(), name="shift-type-list"),
    path("shift-types/<int:pk>/", ShiftTypeDetailView.as_view(), name="shift-type-detail"),

    # スタッフ
    path("staff/", StaffListCreateView.as_view(), name="staff-list"),
    path("staff/<int:pk>/", StaffDetailView.as_view(), name="staff-detail"),

    # 勤務シフト
    path("work-schedules/", WorkScheduleListCreateView.as_view(), name="work-schedule-list"),
    path("work-schedules/<int:pk>/", WorkScheduleDetailView.as_view(), name="work-schedule-detail"),

    # 夜勤の自動登録
    path("assign-night-shift/", assign_night_shift, name="assign-night-shift"),
]
