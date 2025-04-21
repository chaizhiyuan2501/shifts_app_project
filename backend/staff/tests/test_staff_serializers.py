import pytest
from staff.serializers import (
    RoleSerializer,
    StaffSerializer,
    ShiftTypeSerializer,
    WorkScheduleSerializer,
)
from staff.models import Role, Staff, ShiftType, WorkSchedule
from datetime import time, date, timedelta


@pytest.mark.django_db
class TestRoleSerializer:
    def test_valid_data(self):
        serializer = RoleSerializer(data={"name": "介護士"})
        assert serializer.is_valid()
        assert serializer.validated_data["name"] == "介護士"


@pytest.mark.django_db
class TestStaffSerializer:
    def test_name_required(self):
        serializer = StaffSerializer(data={"name": "", "role_id": None})
        assert not serializer.is_valid()
        assert "name" in serializer.errors


@pytest.mark.django_db
class TestShiftTypeSerializer:
    def test_invalid_code(self):
        data = {
            "code": "夜勤@",  # 特殊字符应报错
            "name": "夜勤",
            "start_time": "20:00",
            "end_time": "08:00",
            "break_minutes": 60,
            "color": "#000000",
        }
        serializer = ShiftTypeSerializer(data=data)
        assert not serializer.is_valid()
        assert "code" in serializer.errors

    def test_negative_break_minutes(self):
        data = {
            "code": "YAKIN",
            "name": "夜勤",
            "start_time": "20:00",
            "end_time": "08:00",
            "break_minutes": -1,
            "color": "#000000",
        }
        serializer = ShiftTypeSerializer(data=data)
        assert not serializer.is_valid()
        assert "break_minutes" in serializer.errors


@pytest.mark.django_db
class TestWorkScheduleSerializer:
    def test_past_date_validation(self, django_user_model):
        role, _ = Role.objects.get_or_create(name="看護師")
        user = django_user_model.objects.create(name="test_user")
        staff = Staff.objects.create(name="テスト太郎", role=role, user=user)

        from datetime import timedelta, date

        yesterday = date.today() - timedelta(days=1)
        data = {
            "staff_id": staff.id,
            "shift_id": 1,  # テスト用に既存のシフトIDを使う or 事前に作成する
            "date": str(yesterday),
        }
        serializer = WorkScheduleSerializer(data=data)
        assert not serializer.is_valid()
        assert "date" in serializer.errors
