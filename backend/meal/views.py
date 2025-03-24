from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from .models import MealType, MealOrder
from .serializers import MealTypeSerializer, MealOrderSerializer


class MealTypeViewSet(viewsets.ModelViewSet):
    queryset = MealType.objects.all()
    serializer_class = MealTypeSerializer


class MealOrderViewSet(viewsets.ModelViewSet):
    queryset = MealOrder.objects.all()
    serializer_class = MealOrderSerializer
