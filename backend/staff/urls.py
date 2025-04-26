from django.urls import path
from .views import (
    RoleListCreateView,
    RoleDetailView,
    ShiftTypeListCreateView,
    ShiftTypeDetailView,
    StaffListCreateView,
    StaffDetailView,
    WorkScheduleListCreateView,
    WorkScheduleDetailView,
    assign_night_shift,
)

app_name = "staff"

urlpatterns = [
    path("roles/", RoleListCreateView.as_view(), name="role-list"),  # 役職一覧・作成
    path(
        "roles/<int:pk>/", RoleDetailView.as_view(), name="role-detail"
    ),  # 役職詳細・更新・削除
    path(
        "shift-types/", ShiftTypeListCreateView.as_view(), name="shift-type-list"
    ),  # シフトタイプ一覧・作成
    path(
        "shift-types/<int:pk>/", ShiftTypeDetailView.as_view(), name="shift-type-detail"
    ),  # シフトタイプ詳細・更新・削除
    path(
        "staffs/", StaffListCreateView.as_view(), name="staff-list"
    ),  # スタッフ一覧・作成
    path(
        "staffs/<int:pk>/", StaffDetailView.as_view(), name="staff-detail"
    ),  # スタッフ詳細・更新・削除
    path(
        "schedules/", WorkScheduleListCreateView.as_view(), name="schedule-list"
    ),  # 勤務シフト一覧・作成
    path(
        "schedules/<int:pk>/", WorkScheduleDetailView.as_view(), name="schedule-detail"
    ),  # 勤務シフト詳細・更新・削除
    path(
        "assign-night-shift/", assign_night_shift, name="assign-night-shift"
    ),  # 夜勤の自動割り当て
]
