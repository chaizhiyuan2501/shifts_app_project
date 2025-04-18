from rest_framework.views import APIView
from rest_framework.request import Request
from django.db.models import Count
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from drf_spectacular.utils import extend_schema

from .models import MealType, MealOrder
from meal.serializers import GuestMealOrderSerializer, StaffMealOrderSerializer
from utils.api_response_utils import api_response


@extend_schema(summary="食事種類一覧", tags=["食事管理"])
class MealTypeListCreateAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        meal_types = MealType.objects.all()
        serializer = MealTypeSerializer(meal_types, many=True)
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
class MealTypeDetailAPIView(APIView):
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


@extend_schema(summary="食事注文一覧", tags=["食事管理"])
class MealOrderListCreateAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        orders = MealOrder.objects.all()
        serializer = MealOrderSerializer(orders, many=True)
        return api_response(data=serializer.data)

    def post(self, request):
        serializer = MealOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(code=201, message="作成成功", data=serializer.data)
        return api_response(
            code=400, message="バリデーションエラー", data=serializer.errors
        )


@extend_schema(summary="食事注文詳細", tags=["食事管理"])
class MealOrderDetailAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return MealOrder.objects.get(pk=pk)
        except MealOrder.DoesNotExist:
            return None

    def get(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return api_response(code=404, message="見つかりません")
        serializer = MealOrderSerializer(obj)
        return api_response(data=serializer.data)

    def put(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return api_response(code=404, message="見つかりません")
        serializer = MealOrderSerializer(obj, data=request.data)
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


@extend_schema(summary="指定日付の食事注文数をカウント", tags=["食事管理"])
class MealOrderCountAPIView(APIView):
    def post(self, request: Request):
        """
        リクエスト例:
        {
            "date": "2025-04-20"
        }

        レスポンス例:
        {
            "guest": { "朝食": 5, "昼食": 7, "夕食": 6 },
            "staff": { "昼食": 3, "夕食": 4 },
            "total": { "朝食": 5, "昼食": 10, "夕食": 10 }
        }
        """
        date = request.data.get("date")
        if not date:
            return api_response(code=400, message="dateは必須です")

        meal_types = MealType.objects.values("id", "name", "display_name")
        type_map = {m["id"]: m["display_name"] for m in meal_types}

        # 各グループのカウント
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

        # 整理
        guest_result = {type_map[g["meal_type"]]: g["count"] for g in guest_counts}
        staff_result = {type_map[s["meal_type"]]: s["count"] for s in staff_counts}

        # 合計処理
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

