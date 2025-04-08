import datetime
import pytest
from meal.serializers import MealOrderSerializer
from meal.models import MealType, MealOrder
from guest.models import Guest
from staff.models import Staff

@pytest.mark.django_db
class TestMealOrderSerializer:
    def setup_method(self):
        # テスト用の共通データをセットアップ
        self.meal_type = MealType.objects.create(name="lunch", display_name="昼食")
        self.staff = Staff.objects.create(name="テストスタッフ")
        self.guest = Guest.objects.create(name="テストゲスト")

    def test_valid_staff_order(self):
        """スタッフによる正しい食事注文データがシリアライズ可能であること"""
        valid_data = {
            "date": (datetime.date.today() + datetime.timedelta(days=1)).isoformat(),
            "meal_type_id": self.meal_type.id,
            "staff_id": self.staff.id,
            "ordered": True,
            "auto_generated": False,
            "note": "メモ1",
        }
        serializer = MealOrderSerializer(data=valid_data)
        assert serializer.is_valid(), serializer.errors

    def test_valid_guest_order(self):
        """ゲストによる正しい食事注文データがシリアライズ可能であること"""
        valid_data = {
            "date": (datetime.date.today() + datetime.timedelta(days=1)).isoformat(),
            "meal_type_id": self.meal_type.id,
            "guest_id": self.guest.id,
            "ordered": True,
            "auto_generated": False,
            "note": "メモ2",
        }
        serializer = MealOrderSerializer(data=valid_data)
        assert serializer.is_valid(), serializer.errors

    def test_both_staff_and_guest_error(self):
        """スタッフとゲストの両方が指定された場合はバリデーションエラーになること"""
        invalid_data = {
            "date": (datetime.date.today() + datetime.timedelta(days=1)).isoformat(),
            "meal_type_id": self.meal_type.id,
            "staff_id": self.staff.id,
            "guest_id": self.guest.id,
            "ordered": True,
        }
        serializer = MealOrderSerializer(data=invalid_data)
        assert not serializer.is_valid()
        assert "non_field_errors" in serializer.errors

    def test_neither_staff_nor_guest_error(self):
        """スタッフとゲストの両方が未指定の場合はバリデーションエラーになること"""
        invalid_data = {
            "date": (datetime.date.today() + datetime.timedelta(days=1)).isoformat(),
            "meal_type_id": self.meal_type.id,
            "ordered": True,
        }
        serializer = MealOrderSerializer(data=invalid_data)
        assert not serializer.is_valid()
        assert "non_field_errors" in serializer.errors

    def test_past_date_error(self):
        """過去の日付を指定した場合はバリデーションエラーになること"""
        invalid_data = {
            "date": (datetime.date.today() - datetime.timedelta(days=1)).isoformat(),
            "meal_type_id": self.meal_type.id,
            "staff_id": self.staff.id,
            "ordered": True,
        }
        serializer = MealOrderSerializer(data=invalid_data)
        assert not serializer.is_valid()
        assert "date" in serializer.errors
