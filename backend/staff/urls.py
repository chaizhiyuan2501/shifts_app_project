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

urlpatterns = [
    path("roles/", RoleListCreateView.as_view()),
    path("roles/<int:pk>/", RoleDetailView.as_view()),
    path("shift-types/", ShiftTypeListCreateView.as_view()),
    path("shift-types/<int:pk>/", ShiftTypeDetailView.as_view()),
    path("staffs/", StaffListCreateView.as_view()),
    path("staffs/<int:pk>/", StaffDetailView.as_view()),
    path("schedules/", WorkScheduleListCreateView.as_view()),
    path("schedules/<int:pk>/", WorkScheduleDetailView.as_view()),
    # 夜勤の自動登録
    path("assign-night-shift/", assign_night_shift, name="assign-night-shift"),
]
