import pytest
from rest_framework.test import APIClient
from django.urls import reverse
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
