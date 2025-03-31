import pytest
from datetime import date
from meal.models import MealType, MealOrder
from user.models import User
from staff.models import Staff, Role
from guest.models import Guest


@pytest.mark.django_db
class TestMealModels:

    def setup_method(self):
        # 食事の種類を作成
        self.breakfast = MealType.objects.create(name="朝", display_name="朝食")
        self.lunch = MealType.objects.create(name="昼", display_name="昼食")

        # スタッフと患者を作成
        self.user = User.objects.create_user(name="staffuser", password="1980")
        self.role = Role.objects.create(name="正社員")
        self.staff = Staff.objects.create(user=self.user, full_name="田中太郎", role=self.role)

        self.guest = Guest.objects.create(full_name="山田花子")

        self.today = date.today()

    def test_create_meal_type(self):
        """
        MealType モデルの作成確認テスト
        - name と display_name が保存されていること
        - __str__ が表示名を返すこと
        """
        assert self.breakfast.name == "朝"
        assert self.breakfast.display_name == "朝食"
        assert str(self.breakfast) == "朝食"

    def test_create_meal_order_for_staff(self):
        """
        スタッフに対して MealOrder を作成できるか
        - 正しい日付・食事種別・スタッフが保存されるか
        - __str__ にスタッフ名が含まれるか
        """
        order = MealOrder.objects.create(
            date=self.today,
            meal_type=self.breakfast,
            staff=self.staff,
            ordered=True,
            auto_generated=False,
        )
        assert order.staff.full_name == "田中太郎"
        assert str(order) == f"{self.today} - 田中太郎 - 朝 - ○"  # ○ = ◯ = “○”

    def test_create_meal_order_for_guest(self):
        """
        患者に対して MealOrder を作成できるか
        - 正しい日付・食事種別・患者が保存されるか
        - __str__ に患者名が含まれるか
        """
        order = MealOrder.objects.create(
            date=self.today,
            meal_type=self.lunch,
            guest=self.guest,
            ordered=False,
            auto_generated=True,
        )
        assert order.guest.full_name == "山田花子"
        assert str(order) == f"{self.today} - 山田花子 - 昼 - ×"  # × = “×”

    def test_weekday_jp(self):
        """
        MealOrder の weekday_jp プロパティが日本語で曜日を返すか
        """
        order = MealOrder.objects.create(
            date=date(2025, 3, 28),
            meal_type=self.breakfast,
            staff=self.staff,
        )
        assert order.weekday_jp in ["月", "火", "水", "木", "金", "土", "日"]

    def test_unique_constraint(self):
        """
        guest + date + meal_type の組み合わせが重複した場合にエラーが発生するか
        """
        MealOrder.objects.create(
            date=self.today,
            meal_type=self.breakfast,
            guest=self.guest,
        )
        with pytest.raises(Exception):
            MealOrder.objects.create(
                date=self.today,
                meal_type=self.breakfast,
                guest=self.guest,
            )
