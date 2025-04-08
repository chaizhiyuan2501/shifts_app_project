from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from drf_spectacular.utils import extend_schema

from .models import MealType, MealOrder
from .serializers import MealTypeSerializer, MealOrderSerializer
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
