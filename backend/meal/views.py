from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)

from .models import MealType, MealOrder
from .serializers import MealTypeSerializer, MealOrderSerializer


class MealTypeViewSet(viewsets.ModelViewSet):
    queryset = MealType.objects.all()
    serializer_class = MealTypeSerializer
    permission_classes = [IsAdminUser]


class MealOrderViewSet(viewsets.ModelViewSet):
    queryset = MealOrder.objects.all()
    serializer_class = MealOrderSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
