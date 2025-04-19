from django.urls import path
from .views import (
    MealTypeListCreateView,
    MealTypeDetailView,
    MealOrderListCreateView,
    MealOrderDetailView,
    MealOrderCountView,
)

urlpatterns = [
    path("meal-types/", MealTypeListCreateView.as_view(), name="meal-type-list-create"),
    path("meal-types/<int:pk>/", MealTypeDetailView.as_view(), name="meal-type-detail"),
    path(
        "meal-orders/", MealOrderListCreateView.as_view(), name="meal-order-list-create"
    ),
    path(
        "meal-orders/<int:pk>/", MealOrderDetailView.as_view(), name="meal-order-detail"
    ),
    path("meal-order/count/", MealOrderCountView.as_view(), name="meal-order-count"),
]
