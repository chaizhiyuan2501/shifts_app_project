import pytest
from guest.models import Guest, VisitType, VisitSchedule
from guest.serializers import GuestSerializer, VisitTypeSerializer, VisitScheduleSerializer
from datetime import date, time, timedelta
from django.utils import timezone


@pytest.mark.django_db
class TestGuestSerializer:
    def test_valid_data(self):
        data = {"name": "山田太郎", "birthday": "1980-01-01", "contact": "09012345678", "notes": "メモ"}
        serializer = GuestSerializer(data=data)
        assert serializer.is_valid()
        guest = serializer.save()
        assert guest.name == "山田太郎"

    def test_invalid_name(self):
        data = {"name": "", "birthday": "1980-01-01"}
        serializer = GuestSerializer(data=data)
        assert not serializer.is_valid()
        assert "name" in serializer.errors


@pytest.mark.django_db
class TestVisitTypeSerializer:
    def test_valid_code(self):
        data = {"code": "泊", "name": "泊まり", "color": "#ffcc00"}
        serializer = VisitTypeSerializer(data=data)
        assert serializer.is_valid()

    def test_invalid_code(self):
        data = {"code": "間違い", "name": "無効"}
        serializer = VisitTypeSerializer(data=data)
        assert not serializer.is_valid()
        assert "code" in serializer.errors


@pytest.mark.django_db
class TestVisitScheduleSerializer:
    def test_valid_schedule(self):
        guest = Guest.objects.create(name="テスト", birthday="2000-01-01")
        visit_type = VisitType.objects.create(code="泊", name="泊まり")
        today = timezone.now().date()
        data = {
            "guest_id": guest.id,
            "visit_id": visit_type.id,
            "date": today.isoformat(),
            "arrive_time": "10:00",
            "leave_time": "15:00",
            "note": "特記事項なし"
        }
        serializer = VisitScheduleSerializer(data=data)
        assert serializer.is_valid()
        schedule = serializer.save()
        assert schedule.guest == guest
        assert schedule.visit_type == visit_type

    def test_invalid_date_future(self):
        guest = Guest.objects.create(name="未来人", birthday="1988-01-01")
        visit_type = VisitType.objects.create(code="通い", name="通い")
        tomorrow = timezone.now().date() + timedelta(days=1)
        data = {
            "guest_id": guest.id,
            "visit_id": visit_type.id,
            "date": tomorrow.isoformat()
        }
        serializer = VisitScheduleSerializer(data=data)
        assert not serializer.is_valid()
        assert "date" in serializer.errors