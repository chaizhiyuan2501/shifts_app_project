# staff/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RoleViewSet,
    StaffViewSet,
    ShiftTypeViewSet,
    WorkScheduleViewSet,
    assign_night_shift,
)

router = DefaultRouter()
router.register(r"roles", RoleViewSet)
router.register(r"staff", StaffViewSet)
router.register(r"shifts", ShiftTypeViewSet)
router.register(r"schedules", WorkScheduleViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("assign-night-shift/", assign_night_shift, name="assign-night-shift"),
]
