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

from .models import MealType, MealOrder
from .serializers import MealTypeSerializer, MealOrderSerializer

@extend_schema(
    summary="食事の種類の設定",
    description="",
    tags=["食事管理"],
)
class MealTypeViewSet(viewsets.ModelViewSet):
    queryset = MealType.objects.all()
    serializer_class = MealTypeSerializer
    permission_classes = [IsAdminUser]

@extend_schema(
    summary="食事の注文の設定",
    description="",
    tags=["食事管理"],
)
class MealOrderViewSet(viewsets.ModelViewSet):
    queryset = MealOrder.objects.all()
    serializer_class = MealOrderSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
