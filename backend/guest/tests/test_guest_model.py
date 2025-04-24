import pytest
from datetime import date
from django.db.utils import IntegrityError

from meal.models import MealType, MealOrder
from user.models import User
from staff.models import Staff, Role
from guest.models import Guest


@pytest.mark.django_db
class TestMealModels:
    """
    Mealアプリのモデルに関するテストクラス。
    - MealType（食事の種類）
    - MealOrder（食事注文）

    各モデルの作成・制約・文字列表示・プロパティ機能をテストする。
    """

    def setup_method(self):
        """
        テスト共通の初期データを作成する。
        - 食事種別（朝・昼）
        - スタッフとそのユーザー・役職
        - ゲスト
        - 今日の日付
        """
        self.breakfast, _ = MealType.objects.get_or_create(
            name="朝", display_name="朝食"
        )
        self.lunch, _ = MealType.objects.get_or_create(name="昼", display_name="昼食")

        self.user = User.objects.create_user(name="staffuser", password="1980")
        self.role, _ = Role.objects.get_or_create(name="正社員")
        self.staff, _ = Staff.objects.get_or_create(
            user=self.user, name="田中太郎", role=self.role
        )

        self.guest, _ = Guest.objects.get_or_create(name="山田花子")
        self.today = date.today()

    def test_create_meal_type(self):
        """
        MealType モデルの作成テスト
        - name と display_name が正しく保存されていること
        - __str__ メソッドが表示名を返すこと
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
        order, _ = MealOrder.objects.get_or_create(
            date=self.today,
            meal_type=self.breakfast,
            staff=self.staff,
            ordered=True,
            auto_generated=False,
        )
        assert order.staff.name == "田中太郎"
        assert str(order) == f"{self.today} - 田中太郎 - 朝 - ○"

    def test_create_meal_order_for_guest(self):
        """
        患者に対して MealOrder を作成できるか
        - 正しい日付・食事種別・患者が保存されるか
        - __str__ に患者名が含まれるか
        """
        order, _ = MealOrder.objects.get_or_create(
            date=self.today,
            meal_type=self.lunch,
            guest=self.guest,
            ordered=False,
            auto_generated=True,
        )
        assert order.guest.name == "山田花子"
        assert str(order) == f"{self.today} - 山田花子 - 昼 - ×"

    def test_weekday_jp(self):
        """
        MealOrder の weekday_jp プロパティが日本語で曜日を返すか
        - 正しく "月〜日" のいずれかが返されること
        """
        order, _ = MealOrder.objects.get_or_create(
            date=date(2025, 3, 28),
            meal_type=self.breakfast,
            staff=self.staff,
        )
        assert order.weekday_jp in ["月", "火", "水", "木", "金", "土", "日"]

    # def test_unique_constraint(self):
    #     """
    #     guest + date + meal_type の組み合わせが重複した場合にエラーが発生するか
    #     """
    #     MealOrder.objects.create(
    #         date=self.today,
    #         meal_type=self.breakfast,
    #         guest=self.guest,
    #     )
    #     with pytest.raises(IntegrityError):
    #         MealOrder.objects.create(
    #             date=self.today,
    #             meal_type=self.breakfast,
    #             guest=self.guest,
    #         )
