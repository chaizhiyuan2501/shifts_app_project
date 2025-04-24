import datetime
import pytest
from meal.serializers import GuestMealOrderSerializer, StaffMealOrderSerializer
from meal.models import MealType
from guest.models import Guest
from staff.models import Staff
from user.models import User


@pytest.mark.django_db
class TestMealOrderSerializers:
    """
    Mealアプリのシリアライザに関するテストクラス。
    - StaffMealOrderSerializer
    - GuestMealOrderSerializer

    入力データのバリデーションや、重複注文・日付制約の確認を行う。
    """

    def setup_method(self):
        """
        各テストの前に共通で使用するデータ（スタッフ、ゲスト、食事種別）を作成する。
        """
        self.user = User.objects.create_user(name="テストユーザー", password="1234")
        self.staff = Staff.objects.create(name="テストスタッフ", user=self.user)
        self.guest = Guest.objects.create(name="テストゲスト")
        self.meal_type = MealType.objects.create(name="lunch", display_name="昼食")

    def test_valid_staff_order(self):
        """
        StaffMealOrderSerializer の正常系テスト
        - 正しいスタッフ注文データでバリデーションが通ること
        """
        data = {
            "date": (datetime.date.today() + datetime.timedelta(days=1)).isoformat(),
            "meal_type_id": self.meal_type.id,
            "staff_id": self.staff.id,
            "ordered": True,
        }
        serializer = StaffMealOrderSerializer(data=data)
        assert serializer.is_valid(), serializer.errors

    def test_valid_guest_order(self):
        """
        GuestMealOrderSerializer の正常系テスト
        - 正しいゲスト注文データでバリデーションが通ること
        """
        data = {
            "date": (datetime.date.today() + datetime.timedelta(days=1)).isoformat(),
            "meal_type_id": self.meal_type.id,
            "guest_id": self.guest.id,
            "ordered": True,
        }
        serializer = GuestMealOrderSerializer(data=data)
        assert serializer.is_valid(), serializer.errors

    def test_guest_duplicate_order_error(self):
        """
        GuestMealOrderSerializer の異常系テスト（重複注文）
        - 同一のゲストが同日に同じ食事を2度注文しようとするとエラーになること
        """
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
        """
        StaffMealOrderSerializer の異常系テスト（重複注文）
        - 同一のスタッフが同日に同じ食事を2度注文しようとするとエラーになること
        """
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

    # def test_guest_order_past_date_error(self):
    #     """
    #     GuestMealOrderSerializer の異常系テスト（過去日付）
    #     - ゲスト注文で過去日付が指定された場合にエラーとなること
    #     """
    #     data = {
    #         "date": (datetime.date.today() - datetime.timedelta(days=1)).isoformat(),
    #         "meal_type_id": self.meal_type.id,
    #         "guest_id": self.guest.id,
    #         "ordered": True,
    #     }
    #     serializer = GuestMealOrderSerializer(data=data)
    #     assert not serializer.is_valid()
    #     assert "date" in serializer.errors

    # def test_staff_order_past_date_error(self):
    #     """
    #     StaffMealOrderSerializer の異常系テスト（過去日付）
    #     - スタッフ注文で過去日付が指定された場合にエラーとなること
    #     """
    #     data = {
    #         "date": (datetime.date.today() - datetime.timedelta(days=1)).isoformat(),
    #         "meal_type_id": self.meal_type.id,
    #         "staff_id": self.staff.id,
    #         "ordered": True,
    #     }
    #     serializer = StaffMealOrderSerializer(data=data)
    #     assert not serializer.is_valid()
    #     assert "date" in serializer.errors
