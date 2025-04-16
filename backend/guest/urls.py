from django.urls import path
from .views import (
    GuestListCreateView,
    GuestDetailView,
    VisitTypeListCreateView,
    VisitTypeDetailView,
    VisitScheduleListCreateView,
    VisitScheduleDetailView,
    ScheduleUploadView,
)

app_name = "guest"


urlpatterns = [
    # 利用者（Guest）
    path(
        "guests/", GuestListCreateView.as_view(), name="guest-list-create"
    ),  # GET, POST
    path(
        "guests/<int:pk>/", GuestDetailView.as_view(), name="guest-detail"
    ),  # GET, PUT, DELETE
    # 来訪種別（VisitType）
    path(
        "visit-types/", VisitTypeListCreateView.as_view(), name="visit-type-list-create"
    ),  # GET, POST
    path(
        "visit-types/<int:pk>/", VisitTypeDetailView.as_view(), name="visit-type-detail"
    ),  # GET, PUT, DELETE
    # 来訪スケジュール（VisitSchedule）
    path(
        "schedules/", VisitScheduleListCreateView.as_view(), name="schedule-list-create"
    ),  # GET, POST
    path(
        "schedules/<int:pk>/", VisitScheduleDetailView.as_view(), name="schedule-detail"
    ),  # GET, PUT, DELETE
    # スケジュール画像アップロード（OCR）
    path(
        "schedules/upload/", ScheduleUploadView.as_view(), name="schedule-upload"
    ),  # POST
]
