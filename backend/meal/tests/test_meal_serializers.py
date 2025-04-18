import datetime
import pytest
from meal.serializers import GuestMealOrderSerializer, StaffMealOrderSerializer
from meal.models import MealType
from guest.models import Guest
from staff.models import Staff
from user.models import User


@pytest.mark.django_db
class TestMealOrderSerializers:
    def setup_method(self):
        # 共通のテストデータ
        self.user = User.objects.create_user(name="テストユーザー", password="1234")
        self.staff = Staff.objects.create(name="テストスタッフ", user=self.user)
        self.guest = Guest.objects.create(name="テストゲスト")
        self.meal_type = MealType.objects.create(name="lunch", display_name="昼食")

    def test_valid_staff_order(self):
        """スタッフによる正しい注文"""
        data = {
            "date": (datetime.date.today() + datetime.timedelta(days=1)).isoformat(),
            "meal_type_id": self.meal_type.id,
            "staff_id": self.staff.id,
            "ordered": True,
        }
        serializer = StaffMealOrderSerializer(data=data)
        assert serializer.is_valid(), serializer.errors

    def test_valid_guest_order(self):
        """ゲストによる正しい注文"""
        data = {
            "date": (datetime.date.today() + datetime.timedelta(days=1)).isoformat(),
            "meal_type_id": self.meal_type.id,
            "guest_id": self.guest.id,
            "ordered": True,
        }
        serializer = GuestMealOrderSerializer(data=data)
        assert serializer.is_valid(), serializer.errors

    def test_guest_duplicate_order_error(self):
        """ゲストの同日同種類の重複注文はエラー"""
        from meal.models import MealOrder
        MealOrder.objects.create(
            date=datetime.date.today() + datetime.timedelta(days=1),
            guest=self.guest,
            meal_type=self.meal_type,
        )

        data = {
            "date": (datetime.date.today() + datetime.timedelta(days=1)).isoformat(),
            "meal_type_id": self.meal_type.id,
            "guest_id": self.guest.id,
            "ordered": True,
        }
        serializer = GuestMealOrderSerializer(data=data)
        assert not serializer.is_valid()
        assert "non_field_errors" in serializer.errors

    def test_staff_duplicate_order_error(self):
        """スタッフの同日同種類の重複注文はエラー"""
        from meal.models import MealOrder
        MealOrder.objects.create(
            date=datetime.date.today() + datetime.timedelta(days=1),
            staff=self.staff,
            meal_type=self.meal_type,
        )

        data = {
            "date": (datetime.date.today() + datetime.timedelta(days=1)).isoformat(),
            "meal_type_id": self.meal_type.id,
            "staff_id": self.staff.id,
            "ordered": True,
        }
        serializer = StaffMealOrderSerializer(data=data)
        assert not serializer.is_valid()
        assert "non_field_errors" in serializer.errors

    def test_guest_order_past_date_error(self):
        """ゲストが過去の日付を指定した場合はエラー"""
        data = {
            "date": (datetime.date.today() - datetime.timedelta(days=1)).isoformat(),
            "meal_type_id": self.meal_type.id,
            "guest_id": self.guest.id,
            "ordered": True,
        }
        serializer = GuestMealOrderSerializer(data=data)
        assert not serializer.is_valid()
        assert "date" in serializer.errors

    def test_staff_order_past_date_error(self):
        """スタッフが過去の日付を指定した場合はエラー"""
        data = {
            "date": (datetime.date.today() - datetime.timedelta(days=1)).isoformat(),
            "meal_type_id": self.meal_type.id,
            "staff_id": self.staff.id,
            "ordered": True,
        }
        serializer = StaffMealOrderSerializer(data=data)
        assert not serializer.is_valid()
        assert "date" in serializer.errors
