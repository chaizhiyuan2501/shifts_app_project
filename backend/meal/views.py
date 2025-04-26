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


class MealTypeListCreateView(APIView):
    """
    食事の種類一覧取得・新規登録APIビュー
    """

    permission_classes = [IsAdminUser]

    @extend_schema(
        operation_id="MealTypeList",
        summary="食事種類一覧の取得",
        description="登録済みの食事種類（朝食、昼食、夕食など）を一覧で取得します。",
        tags=["食事管理"],
    )
    def get(self, request):
        queryset = MealType.objects.all()
        serializer = MealTypeSerializer(queryset, many=True)
        return api_response(data=serializer.data)

    @extend_schema(
        operation_id="MealTypeCreate",
        summary="食事種類の新規登録",
        description="新しい食事種類を登録します。",
        tags=["食事管理"],
    )
    def post(self, request):
        serializer = MealTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(code=201, message="作成成功", data=serializer.data)
        return api_response(
            code=400, message="バリデーションエラー", data=serializer.errors
        )


class MealTypeDetailView(APIView):
    """
    食事の種類詳細取得・更新・削除APIビュー
    """

    permission_classes = [IsAdminUser]

    def get_object(self, pk):
        try:
            return MealType.objects.get(pk=pk)
        except MealType.DoesNotExist:
            return None

    @extend_schema(
        operation_id="MealTypeRetrieve",
        summary="食事種類の詳細取得",
        description="特定の食事種類情報を取得します。",
        tags=["食事管理"],
    )
    def get(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return api_response(code=404, message="見つかりません")
        serializer = MealTypeSerializer(obj)
        return api_response(data=serializer.data)

    @extend_schema(
        operation_id="MealTypeUpdate",
        summary="食事種類の更新",
        description="特定の食事種類情報を更新します。",
        tags=["食事管理"],
    )
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

    @extend_schema(
        operation_id="MealTypeDelete",
        summary="食事種類の削除",
        description="特定の食事種類情報を削除します。",
        tags=["食事管理"],
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


class MealOrderListCreateView(APIView):
    """
    食事注文一覧取得・新規登録APIビュー
    """

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self, request):
        if request.user.is_authenticated and hasattr(request.user, "staff"):
            return StaffMealOrderSerializer
        return GuestMealOrderSerializer

    @extend_schema(
        operation_id="MealOrderList",
        summary="食事注文一覧の取得",
        description="すべての食事注文を一覧で取得します。",
        tags=["食事管理"],
    )
    def get(self, request):
        orders = MealOrder.objects.all()
        serializer_class = self.get_serializer_class(request)
        serializer = serializer_class(orders, many=True)
        return api_response(data=serializer.data)

    @extend_schema(
        operation_id="MealOrderCreate",
        summary="食事注文の新規登録",
        description="新しい食事注文を登録します。",
        tags=["食事管理"],
    )
    def post(self, request):
        serializer_class = self.get_serializer_class(request)
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(code=201, message="作成成功", data=serializer.data)
        return api_response(
            code=400, message="バリデーションエラー", data=serializer.errors
        )


class MealOrderDetailView(APIView):
    """
    食事注文詳細取得・更新・削除APIビュー
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

    @extend_schema(
        operation_id="MealOrderRetrieve",
        summary="食事注文の詳細取得",
        description="特定の食事注文情報を取得します。",
        tags=["食事管理"],
    )
    def get(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return api_response(code=404, message="見つかりません")
        serializer_class = self.get_serializer_class(request)
        serializer = serializer_class(obj)
        return api_response(data=serializer.data)

    @extend_schema(
        operation_id="MealOrderUpdate",
        summary="食事注文の更新",
        description="特定の食事注文情報を更新します。",
        tags=["食事管理"],
    )
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

    @extend_schema(
        operation_id="MealOrderDelete",
        summary="食事注文の削除",
        description="特定の食事注文情報を削除します。",
        tags=["食事管理"],
    )
    def delete(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return api_response(code=404, message="見つかりません")
        obj.delete()
        return api_response(code=204, message="削除成功")


class MealOrderCountView(APIView):
    """
    食事注文件数集計APIビュー
    """

    @extend_schema(
        operation_id="MealOrderCount",
        summary="食事注文件数の集計",
        description="指定日付における食事注文の件数をゲスト別・スタッフ別・合計で集計して返します。",
        tags=["食事管理"],
    )
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


class MealOrderAutoGenerateView(APIView):
    """
    食事注文一括自動生成APIビュー
    """

    permission_classes = [IsAdminUser]

    @extend_schema(
        operation_id="MealOrderAutoGenerate",
        summary="食事注文の自動生成",
        description="指定日付のシフトおよび訪問予定に基づき、スタッフと泊の利用者に対して食事注文を自動生成します。",
        tags=["食事管理"],
    )
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
