from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from .models import Guest, VisitType, VisitSchedule
from .serializers import (
    GuestSerializer,
    VisitTypeSerializer,
    VisitScheduleSerializer,
)


class GuestViewSet(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer


class VisitTypeViewSet(viewsets.ModelViewSet):
    queryset = VisitType.objects.all()
    serializer_class = VisitTypeSerializer


class VisitScheduleViewSet(viewsets.ModelViewSet):
    queryset = VisitSchedule.objects.all()
    serializer_class = VisitScheduleSerializer
