# staff/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    GuestViewSet,
    VisitTypeViewSet,
    VisitScheduleViewSet,
)

app_name = "guest"


router = DefaultRouter()
router.register(r"guest", GuestViewSet)
router.register(r"visit-type", VisitTypeViewSet)
router.register(r"visit-schedule", VisitScheduleViewSet)

urlpatterns = [
    path("guest/", include(router.urls)),
]
