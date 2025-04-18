import pytest
from rest_framework.test import APIClient
from user.models import User
from guest.models import Guest, VisitType, VisitSchedule
from datetime import date

from utils.test_utils import unique_code,unique_name

@pytest.mark.django_db
class TestGuestAPIViews:
    def setup_method(self):
        self.client = APIClient()
        self.admin = User.objects.create_superuser(name=unique_name("admin"), password="admin123")
        self.guest = Guest.objects.create(name="テスト利用者", birthday="1970-01-01")
        self.visit_type = VisitType.objects.create(code=unique_code("泊"), name="泊まり")

    def test_guest_list(self):
        self.client.force_authenticate(user=self.admin)
        res = self.client.get("/api/guest/guests/")
        assert res.status_code == 200
        assert isinstance(res.data["data"], list)

    def test_guest_create(self):
        self.client.force_authenticate(user=self.admin)
        data = {"name": "新しいゲスト", "birthday": "1980-02-02"}
        res = self.client.post("/api/guest/guests/", data)
        assert res.status_code == 201
        assert res.data["data"]["name"] == "新しいゲスト"

    def test_guest_update(self):
        self.client.force_authenticate(user=self.admin)
        url = f"/api/guest/guests/{self.guest.id}/"
        res = self.client.put(url, {"name": "更新ゲスト", "birthday": "1970-01-01"})
        assert res.status_code == 200
        assert res.data["data"]["name"] == "更新ゲスト"

    def test_guest_delete(self):
        self.client.force_authenticate(user=self.admin)
        url = f"/api/guest/guests/{self.guest.id}/"
        res = self.client.delete(url)
        assert res.status_code == 204


@pytest.mark.django_db
class TestVisitScheduleViews:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(name=unique_name("user"), password="1234")
        self.guest = Guest.objects.create(name="利用者", birthday="1988-08-08")
        self.visit_type = VisitType.objects.create(code=unique_code("通い"), name="通い")
        self.schedule = VisitSchedule.objects.create(
            guest=self.guest, visit_type=self.visit_type, date=date(2025, 4, 1)
        )

    def test_schedule_list(self):
        self.client.force_authenticate(user=self.user)
        res = self.client.get("/api/guest/schedules/")
        assert res.status_code == 200
        assert "data" in res.data

    def test_schedule_detail(self):
        self.client.force_authenticate(user=self.user)
        res = self.client.get(f"/api/guest/schedules/{self.schedule.id}/")
        assert res.status_code == 200
        assert res.data["data"]["guest"]["name"] == self.guest.name
