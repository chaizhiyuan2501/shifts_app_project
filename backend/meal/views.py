from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.decorators import api_view
from django.db.models import Count
from datetime import datetime

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
    permission_classes = [IsAdminUser]
    model = MealType
    serializer_class = MealTypeSerializer

    @extend_schema(
        operation_id="MealTypeList",
        summary="食事種類一覧の取得",
        tags=["食事管理"],
        responses={200: OpenApiResponse(description="食事種類一覧取得成功")},
    )
    def get(self, request):
        queryset = self.model.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return api_response(data=serializer.data)

    @extend_schema(
        operation_id="MealTypeCreate",
        summary="食事種類の新規登録",
        tags=["食事管理"],
        request=MealTypeSerializer,
        responses={
            201: OpenApiResponse(description="食事種類作成成功"),
            400: OpenApiResponse(description="バリデーションエラー"),
        },
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(code=201, message="作成成功", data=serializer.data)
        return api_response(
            code=400, message="バリデーションエラー", data=serializer.errors
        )


class MealTypeDetailView(APIView):
    permission_classes = [IsAdminUser]
    model = MealType
    serializer_class = MealTypeSerializer

    def get_object(self, pk):
        return self.model.objects.filter(pk=pk).first()

    @extend_schema(
        operation_id="MealTypeRetrieve",
        summary="食事種類の詳細取得",
        tags=["食事管理"],
        responses={
            200: OpenApiResponse(description="食事種類詳細取得成功"),
            404: OpenApiResponse(description="対象データが存在しない"),
        },
    )
    def get(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return api_response(code=404, message="見つかりません")
        serializer = self.serializer_class(obj)
        return api_response(data=serializer.data)

    @extend_schema(
        operation_id="MealTypeUpdate",
        summary="食事種類の更新",
        tags=["食事管理"],
        request=MealTypeSerializer,
        responses={
            200: OpenApiResponse(description="食事種類更新成功"),
            400: OpenApiResponse(description="バリデーションエラー"),
        },
    )
    def put(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return api_response(code=404, message="見つかりません")
        serializer = self.serializer_class(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(message="更新成功", data=serializer.data)
        return api_response(
            code=400, message="バリデーションエラー", data=serializer.errors
        )

    @extend_schema(
        operation_id="MealTypeDelete",
        summary="食事種類の削除",
        tags=["食事管理"],
        responses={
            204: OpenApiResponse(description="食事種類削除成功"),
            404: OpenApiResponse(description="対象データが存在しない"),
        },
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
    permission_classes = [IsAuthenticatedOrReadOnly]
    model = MealOrder

    def get_serializer_class(self, request):
        if request.user.is_authenticated and hasattr(request.user, "staff"):
            return StaffMealOrderSerializer
        return GuestMealOrderSerializer

    @extend_schema(
        operation_id="MealOrderList",
        summary="食事注文一覧の取得",
        tags=["食事管理"],
        responses={200: OpenApiResponse(description="食事注文一覧取得成功")},
    )
    def get(self, request):
        orders = self.model.objects.all()
        serializer_class = self.get_serializer_class(request)
        serializer = serializer_class(orders, many=True)
        return api_response(data=serializer.data)

    @extend_schema(
        operation_id="MealOrderCreate",
        summary="食事注文の新規登録",
        tags=["食事管理"],
        responses={
            201: OpenApiResponse(description="食事注文作成成功"),
            400: OpenApiResponse(description="バリデーションエラー"),
        },
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
    permission_classes = [IsAuthenticatedOrReadOnly]
    model = MealOrder

    def get_object(self, pk):
        return self.model.objects.filter(pk=pk).first()

    def get_serializer_class(self, request):
        if request.user.is_authenticated and hasattr(request.user, "staff"):
            return StaffMealOrderSerializer
        return GuestMealOrderSerializer

    @extend_schema(
        operation_id="MealOrderRetrieve",
        summary="食事注文の詳細取得",
        tags=["食事管理"],
        responses={
            200: OpenApiResponse(description="食事注文詳細取得成功"),
            404: OpenApiResponse(description="対象データが存在しない"),
        },
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
        tags=["食事管理"],
        responses={
            200: OpenApiResponse(description="食事注文更新成功"),
            400: OpenApiResponse(description="バリデーションエラー"),
        },
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
        tags=["食事管理"],
        responses={
            204: OpenApiResponse(description="食事注文削除成功"),
            404: OpenApiResponse(description="対象データが存在しない"),
        },
    )
    def delete(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return api_response(code=404, message="見つかりません")
        obj.delete()
        return api_response(code=204, message="削除成功")


# ========================================
# 特殊操作API（集計、生成）
# ========================================


class MealOrderCountView(APIView):
    permission_classes = [IsAdminUser]

    @extend_schema(
        operation_id="MealOrderCount",
        summary="食事注文件数の集計",
        tags=["食事管理"],
        responses={200: OpenApiResponse(description="食事注文集計成功")},
    )
    def post(self, request):
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
            data={"guest": guest_result, "staff": staff_result, "total": total_result},
        )


# ========================================
# 複数期間の食事注文件数の集計API
# ========================================

class MealOrderCountPeriodsView(APIView):
    permission_classes = [IsAdminUser]

    @extend_schema(
        operation_id="MealOrderCountPeriods",
        summary="複数期間の食事注文集計",
        description="指定された複数の期間に対して、利用者・スタッフ別および合計の食事注文件数を集計します。",
        tags=["食事管理"],
        request={
            "application/json": {
                "example": {
                    "periods": [
                        {"start_date": "2025-04-01", "end_date": "2025-04-07"},
                        {"start_date": "2025-04-15", "end_date": "2025-04-21"}
                    ]
                }
            }
        },
        responses={200: OpenApiResponse(description="複数期間の食事注文集計成功")}
    )
    def post(self, request):
        periods = request.data.get("periods")

        if not periods or not isinstance(periods, list):
            return api_response(code=400, message="periodsは必須で、リスト形式で指定してください")

        # 食事種類マスタを取得（ID→表示名のマッピング）
        meal_types = MealType.objects.values("id", "name", "display_name")
        type_map = {m["id"]: m["display_name"] for m in meal_types}

        results = []

        for period in periods:
            start_date = period.get("start_date")
            end_date = period.get("end_date")

            if not start_date or not end_date:
                continue  # 無効な期間はスキップ

            try:
                start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
                end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
            except ValueError:
                continue  # 日付形式エラーはスキップ

            # 利用者別集計
            guest_counts = (
                MealOrder.objects.filter(date__range=(start_date, end_date), guest__isnull=False)
                .values("meal_type")
                .annotate(count=Count("id"))
            )

            # スタッフ別集計
            staff_counts = (
                MealOrder.objects.filter(date__range=(start_date, end_date), staff__isnull=False)
                .values("meal_type")
                .annotate(count=Count("id"))
            )

            guest_result = {type_map.get(g["meal_type"], "不明"): g["count"] for g in guest_counts}
            staff_result = {type_map.get(s["meal_type"], "不明"): s["count"] for s in staff_counts}

            # 合計を作成
            total_result = {}
            for name in set(guest_result.keys()) | set(staff_result.keys()):
                total_result[name] = guest_result.get(name, 0) + staff_result.get(name, 0)

            results.append({
                "period": {"start": start_date.strftime("%Y-%m-%d"), "end": end_date.strftime("%Y-%m-%d")},
                "guest": guest_result,
                "staff": staff_result,
                "total": total_result,
            })

        return api_response(message="集計成功", data=results)



class MealOrderAutoGenerateView(APIView):
    permission_classes = [IsAdminUser]

    @extend_schema(
        operation_id="MealOrderAutoGenerate",
        summary="食事注文の自動生成",
        tags=["食事管理"],
        responses={200: OpenApiResponse(description="自動生成成功")},
    )
    def post(self, request):
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
