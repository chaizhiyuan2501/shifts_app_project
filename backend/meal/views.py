from rest_framework.views import APIView
from rest_framework.request import Request
from django.db.models import Count
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from drf_spectacular.utils import extend_schema

from .models import MealType, MealOrder
from .serializers import (
    MealTypeSerializer,
    GuestMealOrderSerializer,
    StaffMealOrderSerializer,
)

from utils.api_response_utils import api_response
from meal.utils.order_utils import generate_meal_orders_for_day


# ========================================
# 食事の種類（MealType）API
# ========================================


@extend_schema(summary="食事種類一覧と作成", tags=["食事管理"])
class MealTypeListCreateView(APIView):
    """
    食事の種類（朝・昼・夕）の一覧取得・登録API
    - GET：すべての食事種別を取得（管理者）
    - POST：新しい食事種別を登録（管理者）
    """

    permission_classes = [IsAdminUser]

    def get(self, request):
        queryset = MealType.objects.all()
        serializer = MealTypeSerializer(queryset, many=True)
        return api_response(data=serializer.data)

    def post(self, request):
        serializer = MealTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(code=201, message="作成成功", data=serializer.data)
        return api_response(
            code=400, message="バリデーションエラー", data=serializer.errors
        )


@extend_schema(summary="食事種類詳細", tags=["食事管理"])
class MealTypeDetailView(APIView):
    """
    食事の種類の詳細取得・更新・削除API
    - GET：指定IDの詳細取得
    - PUT：更新
    - DELETE：削除
    - 管理者のみアクセス可
    """

    permission_classes = [IsAdminUser]

    def get_object(self, pk):
        try:
            return MealType.objects.get(pk=pk)
        except MealType.DoesNotExist:
            return None

    def get(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return api_response(code=404, message="見つかりません")
        serializer = MealTypeSerializer(obj)
        return api_response(data=serializer.data)

    def put(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return api_response(code=404, message="見つかりません")
        serializer = MealTypeSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(message="更新成功", data=serializer.data)
        return api_response(
            code=400, message="バリデーションエラー", data=serializer.errors
        )

    def delete(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return api_response(code=404, message="見つかりません")
        obj.delete()
        return api_response(code=204, message="削除成功")


# ========================================
# 食事注文（MealOrder）API
# ========================================


@extend_schema(summary="食事注文一覧・登録", tags=["食事管理"])
class MealOrderListCreateView(APIView):
    """
    食事注文の一覧取得・登録API
    - 利用者 or スタッフのログイン状態によりシリアライザを切替
    - GET：全件取得
    - POST：注文登録
    """

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self, request):
        if request.user.is_authenticated and hasattr(request.user, "staff"):
            return StaffMealOrderSerializer
        return GuestMealOrderSerializer

    def get(self, request):
        orders = MealOrder.objects.all()
        serializer_class = self.get_serializer_class(request)
        serializer = serializer_class(orders, many=True)
        return api_response(data=serializer.data)

    def post(self, request):
        serializer_class = self.get_serializer_class(request)
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(code=201, message="作成成功", data=serializer.data)
        return api_response(
            code=400, message="バリデーションエラー", data=serializer.errors
        )


@extend_schema(summary="食事注文詳細操作", tags=["食事管理"])
class MealOrderDetailView(APIView):
    """
    食事注文の詳細取得・更新・削除API
    - ID指定で操作
    - 利用者・スタッフいずれかの認証が必要
    """

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return MealOrder.objects.get(pk=pk)
        except MealOrder.DoesNotExist:
            return None

    def get_serializer_class(self, request):
        if request.user.is_authenticated and hasattr(request.user, "staff"):
            return StaffMealOrderSerializer
        return GuestMealOrderSerializer

    def get(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return api_response(code=404, message="見つかりません")
        serializer_class = self.get_serializer_class(request)
        serializer = serializer_class(obj)
        return api_response(data=serializer.data)

    def put(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return api_response(code=404, message="見つかりません")
        serializer_class = self.get_serializer_class(request)
        serializer = serializer_class(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(message="更新成功", data=serializer.data)
        return api_response(
            code=400, message="バリデーションエラー", data=serializer.errors
        )

    def delete(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return api_response(code=404, message="見つかりません")
        obj.delete()
        return api_response(code=204, message="削除成功")


@extend_schema(summary="食事注文件数の集計", tags=["食事管理"])
class MealOrderCountView(APIView):
    """
    指定日付における注文件数の集計API
    - ゲスト、スタッフ、全体の食事ごとの件数を返す
    """

    def post(self, request: Request):
        date = request.data.get("date")
        if not date:
            return api_response(code=400, message="dateは必須です")

        meal_types = MealType.objects.values("id", "name", "display_name")
        type_map = {m["id"]: m["display_name"] for m in meal_types}

        guest_counts = (
            MealOrder.objects.filter(date=date, guest__isnull=False)
            .values("meal_type")
            .annotate(count=Count("id"))
        )
        staff_counts = (
            MealOrder.objects.filter(date=date, staff__isnull=False)
            .values("meal_type")
            .annotate(count=Count("id"))
        )

        guest_result = {type_map[g["meal_type"]]: g["count"] for g in guest_counts}
        staff_result = {type_map[s["meal_type"]]: s["count"] for s in staff_counts}

        total_result = {}
        for name in set(guest_result.keys()) | set(staff_result.keys()):
            total_result[name] = guest_result.get(name, 0) + staff_result.get(name, 0)

        return api_response(
            message="カウント成功",
            data={
                "guest": guest_result,
                "staff": staff_result,
                "total": total_result,
            },
        )


@extend_schema(
    summary="食事注文の自動生成",
    description="指定日付のシフトおよび訪問予定に基づき、スタッフおよび「泊」の利用者に対して朝・昼・夕の食事注文を一括生成する。",
    tags=["食事管理"],
)
class MealOrderAutoGenerateView(APIView):
    """
    食事注文の一括自動生成API（管理者用）
    - 指定された日付に対して、スタッフのシフトと「泊」の利用者に基づき注文を作成
    - 利用者の訪問種別が「泊」のみ対象
    """

    permission_classes = [IsAdminUser]

    def post(self, request):
        from datetime import datetime

        date_str = request.data.get("date")
        if not date_str:
            return api_response(code=400, message="dateは必須です")

        try:
            parsed_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return api_response(
                code=400, message="日付の形式が正しくありません（例: 2025-04-20）"
            )

        generate_meal_orders_for_day(parsed_date)

        return api_response(message=f"{date_str} の食事注文を自動生成しました。")
