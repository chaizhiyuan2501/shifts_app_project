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

from .models import Guest, VisitType, VisitSchedule
from .serializers import (
    GuestSerializer,
    VisitTypeSerializer,
    VisitScheduleSerializer,
)

@extend_schema(
    summary="利用者情報の設定",
    description="",
    tags=["利用者管理"],
)
class GuestViewSet(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    permission_classes = [IsAdminUser]

@extend_schema(
    summary="利用者来訪種別の設定",
    description="",
    tags=["利用者管理"],
)
class VisitTypeViewSet(viewsets.ModelViewSet):
    queryset = VisitType.objects.all()
    serializer_class = VisitTypeSerializer
    permission_classes = [IsAdminUser]

@extend_schema(
    summary="利用者来訪スケジュールの設定",
    description="",
    tags=["利用者管理"],
)
class VisitScheduleViewSet(viewsets.ModelViewSet):
    queryset = VisitSchedule.objects.all()
    serializer_class = VisitScheduleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
