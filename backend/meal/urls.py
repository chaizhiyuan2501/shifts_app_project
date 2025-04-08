from django.urls import path
from .views import (
    MealTypeListCreateAPIView,
    MealTypeDetailAPIView,
    MealOrderListCreateAPIView,
    MealOrderDetailAPIView,
)

urlpatterns = [
    # 食事の種類一覧と新規作成エンドポイント
    path(
        "meal-types/", MealTypeListCreateAPIView.as_view(), name="meal-type-list-create"
    ),
    # 食事の種類の詳細取得・更新・削除エンドポイント（<int:pk>は主キー）
    path(
        "meal-types/<int:pk>/", MealTypeDetailAPIView.as_view(), name="meal-type-detail"
    ),
    # 食事注文一覧と新規注文作成エンドポイント
    path(
        "meal-orders/",
        MealOrderListCreateAPIView.as_view(),
        name="meal-order-list-create",
    ),
    # 食事注文の詳細取得・更新・削除エンドポイント
    path(
        "meal-orders/<int:pk>/",
        MealOrderDetailAPIView.as_view(),
        name="meal-order-detail",
    ),
]
