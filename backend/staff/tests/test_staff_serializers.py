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
    """
    RoleSerializerのテストクラス。
    """

    def test_valid_data(self):
        """職種登録シリアライザーのバリデーションテスト"""
        serializer = RoleSerializer(data={"name": "介護士"})
        assert serializer.is_valid()
        assert serializer.validated_data["name"] == "介護士"


@pytest.mark.django_db
class TestStaffSerializer:
    """
    StaffSerializerのテストクラス。
    """

    def test_name_required(self):
        """スタッフ名の空欄バリデーションテスト"""
        serializer = StaffSerializer(data={"name": "", "role_id": None})
        assert not serializer.is_valid()
        assert "name" in serializer.errors


@pytest.mark.django_db
class TestShiftTypeSerializer:
    """
    ShiftTypeSerializerのテストクラス。
    """

    def test_invalid_code(self):
        """シフトコードの形式バリデーション（英数字以外エラー）"""
        data = {
            "code": "夜勤@",  # 特殊記号含む
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
        """休憩時間のマイナス値バリデーション（エラー期待）"""
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
    """
    WorkScheduleSerializerのテストクラス。
    """

    def test_past_date_validation(self, django_user_model):
        """勤務日が過去の場合のバリデーションエラーテスト"""
        role, _ = Role.objects.get_or_create(name="看護師")
        user = django_user_model.objects.create(name="test_user")
        staff = Staff.objects.create(name="テスト太郎", role=role, user=user)

        yesterday = date.today() - timedelta(days=1)
        data = {
            "staff_id": staff.id,
            "shift_id": 1,  # 仮のシフトID
            "date": str(yesterday),
        }
        serializer = WorkScheduleSerializer(data=data)
        assert not serializer.is_valid()
        assert "date" in serializer.errors
