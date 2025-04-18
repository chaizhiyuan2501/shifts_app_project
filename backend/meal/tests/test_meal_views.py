import pytest
from rest_framework.test import APIClient
import datetime
from user.models import User
from meal.models import MealType, MealOrder
from guest.models import Guest


@pytest.mark.django_db
class TestMealViews:
    def setup_method(self):
        self.client = APIClient()
        self.admin = User.objects.create_superuser(name="admin", password="admin123")
        self.user = User.objects.create_user(name="user", password="1234")
        self.guest = Guest.objects.create(name="テスト利用者", birthday="1980-01-01")
        self.meal_type = MealType.objects.create(name="和食")
        self.order = MealOrder.objects.create(
            guest=self.guest, meal_type=self.meal_type, date="2025-04-01"
        )

    def test_get_meal_type_list(self):
        self.client.force_authenticate(user=self.admin)
        res = self.client.get("/api/meal-types/")
        assert res.status_code == 200
        assert isinstance(res.data["data"], list)

    def test_create_meal_type(self):
        self.client.force_authenticate(user=self.admin)
        data = {"name": "洋食"}
        res = self.client.post("/api/meal-types/", data)
        assert res.status_code == 201
        assert res.data["data"]["name"] == "洋食"

    def test_get_meal_type_detail(self):
        self.client.force_authenticate(user=self.admin)
        url = f"/api/meal-types/{self.meal_type.id}/"
        res = self.client.get(url)
        assert res.status_code == 200
        assert res.data["data"]["name"] == self.meal_type.name

    def test_update_meal_type(self):
        self.client.force_authenticate(user=self.admin)
        url = f"/api/meal-types/{self.meal_type.id}/"
        data = {"name": "更新済み"}
        res = self.client.put(url, data)
        assert res.status_code == 200
        assert res.data["data"]["name"] == "更新済み"

    def test_delete_meal_type(self):
        self.client.force_authenticate(user=self.admin)
        url = f"/api/meal-types/{self.meal_type.id}/"
        res = self.client.delete(url)
        assert res.status_code == 204

    def test_get_meal_order_list(self):
        self.client.force_authenticate(user=self.user)
        res = self.client.get("/api/meal-orders/")
        assert res.status_code == 200
        assert isinstance(res.data["data"], list)

    def test_create_meal_order(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "guest": self.guest.id,
            "meal_type": self.meal_type.id,
            "date": "2025-04-15",
        }
        res = self.client.post("/api/meal-orders/", data)
        assert res.status_code == 201
        assert res.data["data"]["guest"] == self.guest.id

    def test_get_meal_order_detail(self):
        self.client.force_authenticate(user=self.user)
        url = f"/api/meal-orders/{self.order.id}/"
        res = self.client.get(url)
        assert res.status_code == 200
        assert res.data["data"]["guest"] == self.guest.id

    def test_update_meal_order(self):
        self.client.force_authenticate(user=self.user)
        url = f"/api/meal-orders/{self.order.id}/"
        data = {
            "guest": self.guest.id,
            "meal_type": self.meal_type.id,
            "date": "2025-04-02",
        }
        res = self.client.put(url, data)
        assert res.status_code == 200
        assert res.data["data"]["date"] == "2025-04-02"

    def test_delete_meal_order(self):
        self.client.force_authenticate(user=self.user)
        url = f"/api/meal-orders/{self.order.id}/"
        res = self.client.delete(url)
        assert res.status_code == 204


@pytest.mark.django_db
class TestMealOrderCountAPIView:
    def setup_method(self):
        self.client = APIClient()

    def test_meal_order_count_success(self):
        # 指定した日付に対してPOSTリクエストを送信し、統計が取得できることを確認する
        target_date = (datetime.date.today() + datetime.timedelta(days=1)).isoformat()
        response = self.client.post("/api/meal-order/count/", {"date": target_date}, format="json")

        assert response.status_code == 200
        assert "guest" in response.data["data"]
        assert "staff" in response.data["data"]
        assert "total" in response.data["data"]

    def test_meal_order_count_missing_date(self):
        # 日付が指定されていない場合、400エラーが返ること
        response = self.client.post("/api/meal-order/count/", {}, format="json")

        assert response.status_code == 400
        assert response.data["message"] == "dateは必須です"