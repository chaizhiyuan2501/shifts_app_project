import pytest
import datetime
from datetime import date, time
from rest_framework.test import APIClient
from datetime import date, timedelta
from django.urls import reverse

from user.models import User
from guest.models import Guest
from staff.models import Staff
from meal.models import MealType, MealOrder
from guest.models import Guest, VisitSchedule, VisitType
from staff.models import Staff, WorkSchedule, Role, ShiftType


@pytest.mark.django_db
class TestMealViews:
    """
    Mealアプリのビュー機能に関する統合テストクラス。
    - MealType（食事の種類）
    - MealOrder（食事注文）

    各エンドポイントのGET/POST/PUT/DELETEに対するレスポンスを検証する。
    """

    def setup_method(self):
        """
        各テスト実行前に共通で使用するテストデータを準備する。
        - 管理者ユーザー・一般ユーザー
        - ゲスト利用者、食事種別、既存の食事注文
        """
        User.objects.all().delete()
        self.client = APIClient()
        self.admin = User.objects.create_superuser(name="admin", password="admin123")
        self.user = User.objects.create_user(name="user", password="1234")
        self.guest = Guest.objects.create(name="テスト利用者", birthday="1980-01-01")
        self.meal_type = MealType.objects.create(name="和食")
        self.order = MealOrder.objects.create(
            guest=self.guest, meal_type=self.meal_type, date="2025-04-01"
        )

    def test_get_meal_type_list(self):
        """
        MealType一覧取得API（GET）のテスト
        - 認証済み管理者としてアクセスできること
        - データ形式がリストであること
        """
        self.client.force_authenticate(user=self.admin)
        res = self.client.get("/api/meal/meal-types/")
        assert res.status_code == 200
        assert isinstance(res.data["data"], list)

    def test_create_meal_type(self):
        """
        MealType作成API（POST）のテスト
        - 有効なデータで201レスポンスが返ること
        """
        self.client.force_authenticate(user=self.admin)
        data = {"name": "洋食", "display_name": "洋食"}
        res = self.client.post("/api/meal/meal-types/", data)
        assert res.status_code == 201

    def test_get_meal_type_detail(self):
        """
        MealType詳細取得API（GET）のテスト
        - 正しいIDでデータを取得できること
        """
        self.client.force_authenticate(user=self.admin)
        url = f"/api/meal/meal-types/{self.meal_type.id}/"
        res = self.client.get(url)
        assert res.status_code == 200
        assert res.data["data"]["name"] == self.meal_type.name

    def test_update_meal_type(self):
        """
        MealType更新API（PUT）のテスト
        - PUTリクエストで更新が成功すること
        """
        self.client.force_authenticate(user=self.admin)
        url = f"/api/meal/meal-types/{self.meal_type.id}/"
        data = {"name": "更新済み", "display_name": "更新済み"}
        res = self.client.put(url, data)
        assert res.status_code == 200

    def test_delete_meal_type(self):
        """
        MealType削除API（DELETE）のテスト
        - 削除リクエストで204レスポンスが返ること
        """
        self.client.force_authenticate(user=self.admin)
        url = f"/api/meal/meal-types/{self.meal_type.id}/"
        res = self.client.delete(url)
        assert res.status_code == 204

    def test_get_meal_order_list(self):
        """
        MealOrder一覧取得API（GET）のテスト
        - 一般ユーザーとして一覧取得ができること
        """
        self.client.force_authenticate(user=self.user)
        res = self.client.get("/api/meal/meal-orders/")
        assert res.status_code == 200
        assert isinstance(res.data["data"], list)

    def test_create_meal_order(self):
        """
        MealOrder作成API（POST）のテスト
        - 明日の注文を作成し、201レスポンスが返ること
        """
        self.client.force_authenticate(user=self.user)
        tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).isoformat()
        data = {
            "guest_id": self.guest.id,
            "meal_type_id": self.meal_type.id,
            "date": tomorrow,
        }
        res = self.client.post("/api/meal/meal-orders/", data)
        print(res.data)
        assert res.status_code == 201

    def test_get_meal_order_detail(self):
        """
        MealOrder詳細取得API（GET）のテスト
        - 正しいIDで注文詳細が取得できること
        """
        self.client.force_authenticate(user=self.user)
        url = f"/api/meal/meal-orders/{self.order.id}/"
        res = self.client.get(url)
        assert res.status_code == 200
        assert res.data["data"]["guest"] == self.guest.id

    def test_update_meal_order(self):
        """
        MealOrder更新API（PUT）のテスト
        - 未来の日付に更新できること
        """
        self.client.force_authenticate(user=self.user)
        future_date = (datetime.date.today() + datetime.timedelta(days=2)).isoformat()
        url = f"/api/meal/meal-orders/{self.order.id}/"
        data = {
            "guest_id": self.guest.id,
            "meal_type_id": self.meal_type.id,
            "date": future_date,
        }
        res = self.client.put(url, data)
        print(res.data)
        assert res.status_code == 200

    def test_delete_meal_order(self):
        """
        MealOrder削除API（DELETE）のテスト
        - 削除成功時に204が返ること
        """
        self.client.force_authenticate(user=self.user)
        url = f"/api/meal/meal-orders/{self.order.id}/"
        res = self.client.delete(url)
        assert res.status_code == 204


@pytest.mark.django_db
class TestMealOrderCountAPIView:
    """
    MealOrderCountView（食事注文集計API）のテストクラス
    - 注文件数の集計結果を確認する
    """

    def setup_method(self):
        User.objects.all().delete()
        self.client = APIClient()
        self.admin = User.objects.create_user(
            name="admin", password="adminpass", is_staff=True, is_active=True
        )
        self.client.force_authenticate(user=self.admin)

    def test_meal_order_count_success(self):
        """
        正常系：日付を指定して注文件数を取得する
        - guest/staff/total の項目が含まれること
        """
        target_date = (datetime.date.today() + datetime.timedelta(days=1)).isoformat()
        response = self.client.post(
            "/api/meal/meal-order/count/", {"date": target_date}, format="json"
        )
        assert response.status_code == 200
        assert "guest" in response.data["data"]
        assert "staff" in response.data["data"]
        assert "total" in response.data["data"]

    def test_meal_order_count_missing_date(self):
        """
        異常系：dateが未指定の場合はエラーが返る
        """
        response = self.client.post("/api/meal/meal-order/count/", {}, format="json")
        assert response.status_code == 400
        assert response.data["message"] == "dateは必須です"


@pytest.mark.django_db
class TestMealOrderAutoGenerateView:
    """
    MealOrderAutoGenerateView（食事注文の自動生成API）のテストクラス。
    - 指定日付が正しく送信された場合、注文が自動生成されることを検証する。
    - 不正な日付形式や未指定の場合に適切なエラーレスポンスが返ることを検証する。
    """

    def setup_method(self):
        User.objects.all().delete()
        # 認証済み管理者ユーザーを作成し、クライアントに設定する
        self.client = APIClient()
        self.admin, _ = User.objects.get_or_create(
            name="admin",
            defaults={
                "password": "admin123",
                "is_superuser": True,
                "is_staff": True,
                "is_admin": True,
            },
        )
        self.client.force_authenticate(user=self.admin)

    def test_generate_success(self):
        """
        正常系：日付を指定してリクエストを送信すると、注文が自動生成される
        """
        target_date = (datetime.date.today() + datetime.timedelta(days=1)).isoformat()
        res = self.client.post(
            "/api/meal/meal-order/auto-generate/", {"date": target_date}
        )
        assert res.status_code == 200
        assert "の食事注文を自動生成しました" in res.data["message"]

    def test_generate_missing_date(self):
        """
        異常系：date を指定しない場合、400エラーとメッセージが返る
        """
        res = self.client.post("/api/meal/meal-order/auto-generate/", {})
        assert res.status_code == 400
        assert res.data["message"] == "dateは必須です"

    def test_generate_invalid_date_format(self):
        """
        異常系：不正な日付フォーマット（YYYY/MM/DDなど）を指定した場合、400エラーが返る
        """
        res = self.client.post(
            "/api/meal/meal-order/auto-generate/", {"date": "2025/04/20"}
        )
        assert res.status_code == 400
        assert res.data["message"] == "日付の形式が正しくありません（例: 2025-04-20）"


@pytest.mark.django_db
class TestMealOrderCountPeriodsView:
    """
    MealOrderCountPeriodsView のテストクラス。
    複数期間にわたる食事注文集計APIの動作を検証する。
    """

    def setup_method(self):
        """
        テストデータを準備する。
        - 管理者ユーザーを作成して認証する
        - MealType（食事種類）を2つ作成する
        - ゲストとスタッフを作成する
        - MealOrder（食事注文）を数件作成する
        """
        User.objects.all().delete()
        self.client = APIClient()

        # 管理者ユーザー作成・ログイン
        self.admin_user = User.objects.create_superuser(
            name="admin", password="testpass123"
        )
        self.client.force_authenticate(user=self.admin_user)

        # 食事種類を作成
        self.meal_type1 = MealType.objects.create(name="lunch", display_name="昼食")
        self.meal_type2 = MealType.objects.create(name="dinner", display_name="夕食")

        # ゲストとスタッフを作成
        self.guest = Guest.objects.create(name="ゲスト太郎")
        self.staff = Staff.objects.create(user=self.admin_user, name="スタッフ花子")

        # 今日と明日の食事注文データを作成
        today = date.today()
        tomorrow = today + timedelta(days=1)

        MealOrder.objects.create(
            guest=self.guest, meal_type=self.meal_type1, date=today
        )
        MealOrder.objects.create(
            guest=self.guest, meal_type=self.meal_type2, date=today
        )
        MealOrder.objects.create(
            staff=self.staff, meal_type=self.meal_type1, date=tomorrow
        )

    def test_count_periods_success(self):
        """
        正常系テスト：複数期間を指定して食事注文を正しく集計できること。
        """
        today = date.today()
        tomorrow = today + timedelta(days=1)

        url = reverse("meal:mealorder-count-periods")
        payload = {
            "periods": [
                {
                    "start_date": today.strftime("%Y-%m-%d"),
                    "end_date": today.strftime("%Y-%m-%d"),
                },
                {
                    "start_date": tomorrow.strftime("%Y-%m-%d"),
                    "end_date": tomorrow.strftime("%Y-%m-%d"),
                },
            ]
        }

        res = self.client.post(url, payload, format="json")

        assert res.status_code == 200
        assert res.data["code"] == 200
        assert res.data["message"] == "集計成功"
        assert len(res.data["data"]) == 2  # 2期間分のデータが返る

    def test_count_periods_invalid_format(self):
        """
        異常系テスト：不正なリクエスト形式（periodsなし）に対してエラーが返ること。
        """
        url = reverse("meal:mealorder-count-periods")
        payload = {}  # periodsを省略

        res = self.client.post(url, payload, format="json")

        assert res.status_code == 400
        assert res.data["code"] == 400
        assert res.data["message"] == "periodsは必須で、リスト形式で指定してください"

    def test_count_periods_invalid_date(self):
        """
        異常系テスト：日付フォーマットが間違っている場合にスキップされること。
        """
        url = reverse("meal:mealorder-count-periods")
        payload = {
            "periods": [
                {
                    "start_date": "2025/04/01",
                    "end_date": "2025/04/07",
                },  # 不正なフォーマット
                {"start_date": "2025-04-15", "end_date": "2025-04-21"},
            ]
        }

        res = self.client.post(url, payload, format="json")

        assert res.status_code == 200
        assert res.data["code"] == 200
        assert res.data["message"] == "集計成功"
        assert len(res.data["data"]) == 1  # 有効な1期間分だけ集計される


@pytest.mark.django_db
class TestMealOrderAutoGenerateView:
    """
    MealOrderAutoGenerateView の自動生成と集計処理のテスト。
    ゲスト（泊・通）とスタッフ（日勤・夜勤）のシナリオで食事件数を検証する。
    """

    def setup_method(self):
        User.objects.all().delete()
        self.client = APIClient()

        # 管理者ユーザー作成・認証
        self.admin_user = User.objects.create_superuser(name="admin", password="pass")
        self.client.force_authenticate(user=self.admin_user)

        # 対象日
        self.today = date(2025, 4, 28)

        # 食事種類（朝・昼・夕）作成
        self.breakfast, _ = MealType.objects.get_or_create(
            name="朝", defaults={"display_name": "朝食"}
        )
        self.lunch, _ = MealType.objects.get_or_create(
            name="昼", defaults={"display_name": "昼食"}
        )
        self.dinner, _ = MealType.objects.get_or_create(
            name="夕", defaults={"display_name": "夕食"}
        )

        # 訪問区分「泊」「通」作成
        self.stay_type, _ = VisitType.objects.get_or_create(
            code="泊", defaults={"name": "宿泊"}
        )
        self.day_type, _ = VisitType.objects.get_or_create(
            code="通", defaults={"name": "通い"}
        )

        # ゲスト作成
        self.stay_guest1 = Guest.objects.create(name="泊まり1")
        self.stay_guest2 = Guest.objects.create(name="泊まり2")
        self.day_guest = Guest.objects.create(name="通いゲスト")

        VisitSchedule.objects.create(
            guest=self.stay_guest1,
            date=self.today,
            visit_type=self.stay_type,
            arrive_time=time(10, 0),
            leave_time=time(18, 0),
        )
        VisitSchedule.objects.create(
            guest=self.stay_guest2,
            date=self.today,
            visit_type=self.stay_type,
            arrive_time=time(9, 0),
            leave_time=time(17, 0),
        )
        VisitSchedule.objects.create(
            guest=self.day_guest,
            date=self.today,
            visit_type=self.day_type,
            arrive_time=time(9, 30),
            leave_time=time(14, 0),
        )

        # シフト（スタッフ）作成
        role = Role.objects.create(name="介護士")
        self.staff1_user = User.objects.create_user(name="daystaff", password="pass")
        self.staff2_user = User.objects.create_user(name="nightstaff", password="pass")

        self.staff1 = Staff.objects.create(
            user=self.staff1_user, name="日勤スタッフ", role=role
        )
        self.staff2 = Staff.objects.create(
            user=self.staff2_user, name="夜勤スタッフ", role=role
        )

        self.day_shift, _ = ShiftType.objects.get_or_create(
            code="日",
            defaults={
                "name": "日勤",
                "start_time": time(9, 0),
                "end_time": time(18, 0),
                "break_minutes": 60,
            },
        )
        self.night_shift, _ = ShiftType.objects.get_or_create(
            code="夜",
            defaults={
                "name": "夜勤",
                "start_time": time(17, 0),
                "end_time": time(9, 0),
                "break_minutes": 120,
            },
        )

        WorkSchedule.objects.create(
            staff=self.staff1, date=self.today, shift=self.day_shift
        )
        WorkSchedule.objects.create(
            staff=self.staff2, date=self.today, shift=self.night_shift
        )

    def test_generate_meal_orders_and_count(self):
        """
        正常系テスト：泊まり2人・通い1人・日勤1人・夜勤1人 → 正しい件数が返る
        """
        url = reverse("meal:meal-order-auto-generate")
        response = self.client.post(
            url, {"date": self.today.strftime("%Y-%m-%d")}, format="json"
        )

        assert response.status_code == 200
        data = response.data["data"]

        assert data["guest"] == {
            "朝食": 2,
            "昼食": 3,
            "夕食": 2,
        }  # 泊2人 * 3 + 通1人 * 昼
        assert data["staff"] == {"昼食": 1, "夕食": 1}  # 日勤1人 昼、夜勤1人 夕
        assert data["total"] == {"朝食": 2, "昼食": 4, "夕食": 3}
