import pytest
import datetime
from rest_framework.test import APIClient
from user.models import User
from guest.models import Guest
from meal.models import MealType, MealOrder


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
