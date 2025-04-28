from django.urls import path
from .views import (
    MealTypeListCreateView,
    MealTypeDetailView,
    MealOrderListCreateView,
    MealOrderDetailView,
    MealOrderCountView,
    MealOrderAutoGenerateView,
    MealOrderCountPeriodsView,
)

app_name = "meal"

# =============================
# meal アプリの URL ルーティング定義
# =============================
# 各 URL に対して対応するビューをマッピングし、
# 管理対象となるエンドポイントを定義

urlpatterns = [
    # 食事の種類（MealType）API
    path(
        "meal-types/",
        MealTypeListCreateView.as_view(),
        name="meal-type-list-create",  # GET: 一覧取得, POST: 新規登録
    ),
    path(
        "meal-types/<int:pk>/",
        MealTypeDetailView.as_view(),
        name="meal-type-detail",  # GET: 詳細取得, PUT: 更新, DELETE: 削除
    ),
    # 食事注文（MealOrder）API
    path(
        "meal-orders/",
        MealOrderListCreateView.as_view(),
        name="meal-order-list-create",  # GET: 一覧取得, POST: 新規登録
    ),
    path(
        "meal-orders/<int:pk>/",
        MealOrderDetailView.as_view(),
        name="meal-order-detail",  # GET: 詳細取得, PUT: 更新, DELETE: 削除
    ),
    # 注文件数カウントAPI
    path(
        "meal-order/count/",
        MealOrderCountView.as_view(),
        name="meal-order-count",  # POST: 件数を集計して返す
    ),
    # 自動生成（泊の患者＋スタッフ）API
    path(
        "meal-order/auto-generate/",
        MealOrderAutoGenerateView.as_view(),
        name="meal-order-auto-generate",  # POST: 指定日付の食事注文を一括生成),
    ),
    # 期間を指定し、期間内の食事数をカウントAPI
    path('meal-orders/count-periods/', MealOrderCountPeriodsView.as_view(), name='mealorder-count-periods'),

]
