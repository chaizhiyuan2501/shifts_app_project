import pytest
from guest.models import Guest, VisitType
from guest.serializers import (
    GuestSerializer,
    VisitTypeSerializer,
    VisitScheduleSerializer,
)
from datetime import timedelta
from django.utils import timezone


@pytest.mark.django_db
class TestGuestSerializer:
    """
    GuestSerializer に関するテストクラス。
    - ゲスト情報のバリデーションと保存処理を確認する。
    """

    def test_valid_data(self):
        """
        有効なデータがバリデーションを通過し、保存されることを確認。
        """
        data = {
            "name": "山田太郎",
            "birthday": "1980-01-01",
            "contact": "09012345678",
            "notes": "メモ",
        }
        serializer = GuestSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        guest = serializer.save()
        assert guest.name == "山田太郎"

    def test_invalid_name(self):
        """
        name フィールドが空の場合にバリデーションエラーとなることを確認。
        """
        data = {"name": "", "birthday": "1980-01-01"}
        serializer = GuestSerializer(data=data)
        assert not serializer.is_valid()
        assert "name" in serializer.errors


@pytest.mark.django_db
class TestVisitTypeSerializer:
    """
    VisitTypeSerializer に関するテストクラス。
    - コードや名称の妥当性を検証する。
    """

    def test_valid_code(self):
        """
        有効なコードで VisitType がバリデーションに通ることを確認。
        """
        VisitType.objects.filter(code="泊").delete()  # 重複を避けるために事前削除
        data = {"code": "泊", "name": "泊まり", "color": "#ffcc00"}
        serializer = VisitTypeSerializer(data=data)
        assert serializer.is_valid(), serializer.errors

    def test_invalid_code(self):
        """
        無効なコード（定義されていない値）でバリデーションエラーとなることを確認。
        """
        data = {"code": "間違い", "name": "無効"}
        serializer = VisitTypeSerializer(data=data)
        assert not serializer.is_valid()
        assert "code" in serializer.errors


@pytest.mark.django_db
class TestVisitScheduleSerializer:
    """
    VisitScheduleSerializer に関するテストクラス。
    - スケジュールデータの保存とバリデーションを確認。
    """

    def test_valid_schedule(self):
        """
        正しいスケジュールデータが保存できることを確認。
        """
        guest = Guest.objects.create(name="テスト", birthday="2000-01-01")
        visit_type, _ = VisitType.objects.get_or_create(
            code="泊", defaults={"name": "泊まり", "color": "#cccccc"}
        )
        today = timezone.now().date()
        data = {
            "guest_id": guest.id,
            "visit_type_id": visit_type.id,
            "date": today.isoformat(),
            "arrive_time": "10:00",
            "leave_time": "15:00",
            "note": "特記事項なし",
        }
        serializer = VisitScheduleSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        schedule = serializer.save()
        assert schedule.guest == guest
        assert schedule.visit_type == visit_type

    # def test_invalid_date_future(self):
    #     """
    #     明日以降の日付でスケジュールを登録しようとするとエラーになることを確認。
    #     """
    #     guest = Guest.objects.create(name="未来人", birthday="1988-01-01")
    #     visit_type, _ = VisitType.objects.get_or_create(
    #         code="通い", defaults={"name": "通い", "color": "#cccccc"}
    #     )
    #     tomorrow = timezone.now().date() + timedelta(days=1)
    #     data = {
    #         "guest": guest.id,
    #         "visit_type": visit_type.id,
    #         "date": tomorrow.isoformat(),
    #     }
    #     serializer = VisitScheduleSerializer(data=data)
    #     assert not serializer.is_valid()
    #     assert "date" in serializer.errors
