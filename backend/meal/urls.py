# staff/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MealTypeViewSet,
    MealOrderViewSet,
)

router = DefaultRouter()
router.register(r"meal-type", MealTypeViewSet)
router.register(r"meal-order", MealOrderViewSet)


urlpatterns = [
    path("meal/", include(router.urls)),
]
