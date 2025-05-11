from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from drf_spectacular.utils import extend_schema, OpenApiResponse

import tempfile
from utils.api_response_utils import api_response
from guest.utils.ocr_utils import ScheduleOCRProcessor

from .models import Guest, VisitType, VisitSchedule
from .serializers import (
    GuestSerializer,
    VisitTypeSerializer,
    VisitScheduleSerializer,
    ScheduleUploadSerializer,
)

# ------------------------- 利用者管理 -------------------------


class GuestListCreateView(APIView):
    permission_classes = [IsAdminUser]
    model = Guest
    serializer_class = GuestSerializer

    @extend_schema(
        operation_id="GuestList",
        summary="利用者一覧の取得",
        tags=["利用者管理"],
        responses={200: OpenApiResponse(description="利用者一覧取得成功")},
    )
    def get(self, request):
        guests = self.model.objects.all()
        serializer = self.serializer_class(guests, many=True)
        return api_response(data=serializer.data)

    @extend_schema(
        operation_id="GuestCreate",
        summary="利用者の新規登録",
        tags=["利用者管理"],
        request=GuestSerializer,
        responses={
            201: OpenApiResponse(description="利用者登録成功"),
            400: OpenApiResponse(description="バリデーションエラー"),
        },
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(
                data=serializer.data, message="登録成功", code=status.HTTP_201_CREATED
            )
        return api_response(
            code=status.HTTP_400_BAD_REQUEST, message="登録失敗", data=serializer.errors
        )


class GuestDetailView(APIView):
    permission_classes = [IsAdminUser]
    model = Guest
    serializer_class = GuestSerializer

    def get_object(self, pk):
        return self.model.objects.get(pk=pk)

    @extend_schema(
        operation_id="GuestRetrieve",
        summary="利用者の詳細取得",
        tags=["利用者管理"],
        responses={
            200: OpenApiResponse(description="利用者詳細取得成功"),
            404: OpenApiResponse(description="該当利用者が存在しない"),
        },
    )
    def get(self, request, pk):
        guest = self.get_object(pk)
        serializer = self.serializer_class(guest)
        return api_response(data=serializer.data)

    @extend_schema(
        operation_id="GuestUpdate",
        summary="利用者情報の更新",
        tags=["利用者管理"],
        request=GuestSerializer,
        responses={
            200: OpenApiResponse(description="利用者更新成功"),
            400: OpenApiResponse(description="バリデーションエラー"),
        },
    )
    def put(self, request, pk):
        guest = self.get_object(pk)
        serializer = self.serializer_class(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(data=serializer.data, message="更新成功")
        return api_response(
            code=status.HTTP_400_BAD_REQUEST, message="更新失敗", data=serializer.errors
        )

    @extend_schema(
        operation_id="GuestDelete",
        summary="利用者の削除",
        tags=["利用者管理"],
        responses={
            204: OpenApiResponse(description="利用者削除成功"),
            404: OpenApiResponse(description="該当利用者が存在しない"),
        },
    )
    def delete(self, request, pk):
        guest = self.get_object(pk)
        guest.delete()
        return api_response(message="削除成功", code=status.HTTP_204_NO_CONTENT)


# ------------------------- 来訪種別管理 -------------------------


class VisitTypeListCreateView(APIView):
    permission_classes = [IsAdminUser]
    model = VisitType
    serializer_class = VisitTypeSerializer

    @extend_schema(
        operation_id="VisitTypeList",
        summary="来訪種別一覧の取得",
        tags=["利用者管理"],
        responses={200: OpenApiResponse(description="来訪種別一覧取得成功")},
    )
    def get(self, request):
        types = self.model.objects.all()
        serializer = self.serializer_class(types, many=True)
        return api_response(data=serializer.data)

    @extend_schema(
        operation_id="VisitTypeCreate",
        summary="来訪種別の新規登録",
        tags=["利用者管理"],
        request=VisitTypeSerializer,
        responses={
            201: OpenApiResponse(description="来訪種別登録成功"),
            400: OpenApiResponse(description="バリデーションエラー"),
        },
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(
                data=serializer.data, message="登録成功", code=status.HTTP_201_CREATED
            )
        return api_response(
            code=status.HTTP_400_BAD_REQUEST, message="登録失敗", data=serializer.errors
        )


class VisitTypeDetailView(APIView):
    permission_classes = [IsAdminUser]
    model = VisitType
    serializer_class = VisitTypeSerializer

    def get_object(self, pk):
        return self.model.objects.get(pk=pk)

    @extend_schema(
        operation_id="VisitTypeRetrieve",
        summary="来訪種別の詳細取得",
        tags=["利用者管理"],
        responses={
            200: OpenApiResponse(description="来訪種別詳細取得成功"),
            404: OpenApiResponse(description="該当来訪種別が存在しない"),
        },
    )
    def get(self, request, pk):
        obj = self.get_object(pk)
        serializer = self.serializer_class(obj)
        return api_response(data=serializer.data)

    @extend_schema(
        operation_id="VisitTypeUpdate",
        summary="来訪種別の更新",
        tags=["利用者管理"],
        request=VisitTypeSerializer,
        responses={
            200: OpenApiResponse(description="来訪種別更新成功"),
            400: OpenApiResponse(description="バリデーションエラー"),
        },
    )
    def put(self, request, pk):
        obj = self.get_object(pk)
        serializer = self.serializer_class(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(data=serializer.data, message="更新成功")
        return api_response(
            code=status.HTTP_400_BAD_REQUEST, message="更新失敗", data=serializer.errors
        )

    @extend_schema(
        operation_id="VisitTypeDelete",
        summary="来訪種別の削除",
        tags=["利用者管理"],
        responses={
            204: OpenApiResponse(description="来訪種別削除成功"),
            404: OpenApiResponse(description="該当来訪種別が存在しない"),
        },
    )
    def delete(self, request, pk):
        obj = self.get_object(pk)
        obj.delete()
        return api_response(message="削除成功", code=status.HTTP_204_NO_CONTENT)


# ------------------------- スケジュール管理 -------------------------


class VisitScheduleListCreateView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    model = VisitSchedule
    serializer_class = VisitScheduleSerializer

    @extend_schema(
        operation_id="VisitScheduleList",
        summary="スケジュール一覧の取得",
        tags=["利用者管理"],
        responses={200: OpenApiResponse(description="スケジュール一覧取得成功")},
    )
    def get(self, request):
        qs = self.model.objects.all()
        serializer = self.serializer_class(qs, many=True)
        return api_response(data=serializer.data)

    @extend_schema(
        operation_id="VisitScheduleCreate",
        summary="スケジュールの新規登録",
        tags=["利用者管理"],
        request=VisitScheduleSerializer,
        responses={
            201: OpenApiResponse(description="スケジュール登録成功"),
            400: OpenApiResponse(description="バリデーションエラー"),
        },
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(
                data=serializer.data, message="登録成功", code=status.HTTP_201_CREATED
            )
        return api_response(
            code=status.HTTP_400_BAD_REQUEST, message="登録失敗", data=serializer.errors
        )


class VisitScheduleDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    model = VisitSchedule
    serializer_class = VisitScheduleSerializer

    def get_object(self, pk):
        return self.model.objects.get(pk=pk)

    @extend_schema(
        operation_id="VisitScheduleRetrieve",
        summary="スケジュールの詳細取得",
        tags=["利用者管理"],
        responses={
            200: OpenApiResponse(description="スケジュール詳細取得成功"),
            404: OpenApiResponse(description="該当スケジュールが存在しない"),
        },
    )
    def get(self, request, pk):
        obj = self.get_object(pk)
        serializer = self.serializer_class(obj)
        return api_response(data=serializer.data)

    @extend_schema(
        operation_id="VisitScheduleUpdate",
        summary="スケジュールの更新",
        tags=["利用者管理"],
        request=VisitScheduleSerializer,
        responses={
            200: OpenApiResponse(description="スケジュール更新成功"),
            400: OpenApiResponse(description="バリデーションエラー"),
        },
    )
    def put(self, request, pk):
        obj = self.get_object(pk)
        serializer = self.serializer_class(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(data=serializer.data, message="更新成功")
        return api_response(
            code=status.HTTP_400_BAD_REQUEST, message="更新失敗", data=serializer.errors
        )

    @extend_schema(
        operation_id="VisitScheduleDelete",
        summary="スケジュールの削除",
        tags=["利用者管理"],
        responses={
            204: OpenApiResponse(description="スケジュール削除成功"),
            404: OpenApiResponse(description="該当スケジュールが存在しない"),
        },
    )
    def delete(self, request, pk):
        obj = self.get_object(pk)
        obj.delete()
        return api_response(message="削除成功", code=status.HTTP_204_NO_CONTENT)


# ------------------------- OCRによるスケジュールアップロード -------------------------


class ScheduleUploadView(APIView):
    permission_classes = [IsAdminUser]
    serializer_class = ScheduleUploadSerializer

    @extend_schema(
        operation_id="ScheduleUploadCreate",
        summary="画像からスケジュールの一括登録",
        description="画像ファイルをOCR解析し、スケジュール情報を一括登録します。",
        tags=["利用者管理"],
        request=ScheduleUploadSerializer,
        responses={
            200: OpenApiResponse(description="OCR解析成功"),
            400: OpenApiResponse(description="画像ファイルエラー"),
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return api_response(
                code=status.HTTP_400_BAD_REQUEST,
                message="画像ファイルが無効です。",
                data=serializer.errors,
            )

        image_file = serializer.validated_data["image"]

        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            temp_file.write(image_file.read())
            temp_path = temp_file.name

        processor = ScheduleOCRProcessor(temp_path)
        result = processor.run()

        return api_response(
            message=f"{result['count']}件の訪問スケジュールを登録しました。",
            data={
                "guest": result["guest"],
                "year": result["year"],
                "month": result["month"],
            },
        )
