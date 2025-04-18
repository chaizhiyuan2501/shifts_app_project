import pytest
from rest_framework.test import APIClient
from staff.models import Role, Staff, ShiftType, WorkSchedule
from datetime import date, time

client = APIClient()

@pytest.mark.django_db
class TestRoleView:
    def test_create_role(self, admin_user):
        client.force_authenticate(user=admin_user)
        response = client.post("/api/staff/roles/", {"name": "介護福祉士"})
        assert response.status_code == 201
        assert response.data["message"] == "職種を登録しました。"

    def test_get_role_list(self, admin_user):
        Role.objects.create(name="看護師")
        client.force_authenticate(user=admin_user)
        response = client.get("/api/staff/roles/")
        assert response.status_code == 200
        assert "data" in response.data


@pytest.mark.django_db
class TestStaffView:
    def test_create_staff(self, admin_user):
        role = Role.objects.create(name="看護師")
        client.force_authenticate(user=admin_user)
        data = {"name": "山田太郎", "role_id": role.id}
        response = client.post("/api/staff/staffs/", data)
        assert response.status_code == 201
        assert response.data["data"]["name"] == "山田太郎"

    def test_get_staff_detail(self, admin_user):
        role = Role.objects.create(name="看護師")
        staff = Staff.objects.create(name="佐藤次郎", role=role)
        client.force_authenticate(user=admin_user)
        response = client.get(f"/api/staff/staffs/{staff.id}/")
        assert response.status_code == 200
        assert response.data["data"]["name"] == "佐藤次郎"


@pytest.mark.django_db
class TestShiftTypeView:
    def test_create_shift_type(self, admin_user):
        data = {
            "code": "D",
            "name": "日勤",
            "start_time": "09:00",
            "end_time": "17:00",
            "break_minutes": 60,
            "color": "#FF0000",
        }
        client.force_authenticate(user=admin_user)
        response = client.post("/api/staff/shifts/", data)
        assert response.status_code == 201
        assert response.data["message"] == "シフト種類を登録しました。"


@pytest.mark.django_db
class TestWorkScheduleView:
    def test_create_schedule(self, admin_user):
        role = Role.objects.create(name="介護士")
        staff = Staff.objects.create(name="田中", role=role)
        shift = ShiftType.objects.create(
            code="A", name="早番", start_time=time(7), end_time=time(15), break_minutes=60, color="#123456"
        )
        data = {"staff_id": staff.id, "shift_id": shift.id, "date": str(date.today())}
        client.force_authenticate(user=admin_user)
        response = client.post("/api/staff/schedules/", data)
        assert response.status_code == 201
        assert response.data["message"] == "勤務シフトを登録しました。"
