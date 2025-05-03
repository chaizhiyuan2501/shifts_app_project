import pytest
from rest_framework.test import APIClient
from staff.models import Role, Staff, ShiftType, WorkSchedule
from datetime import date

client = APIClient()


@pytest.mark.django_db
class TestRoleView:
    """
    Role APIエンドポイントのテストクラス。
    """

    def test_create_role(self, admin_user):
        """職種登録APIの成功テスト"""
        client.force_authenticate(user=admin_user)
        response = client.post("/api/staff/roles/", {"name": "介護福祉士"})
        assert response.status_code == 201
        assert response.data["message"] == "職種を登録しました。"

    def test_get_role_list(self, admin_user):
        """職種一覧取得APIの成功テスト"""
        Role.objects.get_or_create(name="看護師")
        client.force_authenticate(user=admin_user)
        response = client.get("/api/staff/roles/")
        assert response.status_code == 200
        assert "data" in response.data


@pytest.mark.django_db
class TestStaffView:
    """
    Staff APIエンドポイントのテストクラス。
    """

    def test_create_staff(self, admin_user):
        """スタッフ登録APIの成功テスト"""
        role, _ = Role.objects.get_or_create(name="看護師")
        client.force_authenticate(user=admin_user)
        data = {"name": "山田太郎", "role_id": role.id, "user_id": admin_user.id}
        response = client.post("/api/staff/staffs/", data)
        assert response.status_code == 201
        assert response.data["data"]["name"] == "山田太郎"

    def test_get_staff_detail(self, admin_user):
        """スタッフ詳細取得APIの成功テスト"""
        role, _ = Role.objects.get_or_create(name="看護師")
        staff = Staff.objects.create(name="テスト太郎", role=role, user=admin_user)
        client.force_authenticate(user=admin_user)
        response = client.get(f"/api/staff/staffs/{staff.id}/")
        assert response.status_code == 200
        assert response.data["data"]["name"] == "テスト太郎"


@pytest.mark.django_db
class TestShiftTypeView:
    """
    ShiftType APIエンドポイントのテストクラス。
    """

    def test_create_shift_type(self, admin_user):
        """シフト種類登録APIの成功テスト"""
        data = {
            "code": "D",
            "name": "日勤",
            "start_time": "09:00",
            "end_time": "17:00",
            "break_minutes": 60,
            "color": "#FF0000",
        }
        client.force_authenticate(user=admin_user)
        response = client.post("/api/staff/shift-types/", data)
        assert response.status_code == 201
        assert response.data["message"] == "シフト種類を登録しました。"


@pytest.mark.django_db
class TestWorkScheduleView:
    """
    WorkSchedule APIエンドポイントのテストクラス。
    """

    def test_create_schedule(self, admin_user):
        """
        勤務シフト登録APIの成功テスト（通常シフト）
        """
        # 既存のShiftType（日1）を使う
        shift = ShiftType.objects.get(code="日1")

        role, _ = Role.objects.get_or_create(name="介護士")
        staff = Staff.objects.create(name="テスト太郎", role=role, user=admin_user)

        data = {"staff_id": staff.id, "shift_id": shift.id, "date": str(date.today())}
        client.force_authenticate(user=admin_user)
        response = client.post("/api/staff/schedules/", data)
        print("response.data:", response.data)

        assert response.status_code == 201
        assert response.data["message"] == "勤務シフトを登録しました。"

    def test_create_night_shift_schedule(self, admin_user):
        """
        夜勤シフト登録APIの成功テスト（夜→明→休3日連続登録）
        """
        # 夜勤用ShiftTypeを確認・取得
        night_shift = ShiftType.objects.get(code="夜")

        role, _ = Role.objects.get_or_create(name="介護士")
        staff = Staff.objects.create(name="テスト花子", role=role, user=admin_user)

        client.force_authenticate(user=admin_user)
        data = {
            "staff_id": staff.id,
            "shift_id": night_shift.id,
            "date": str(date.today()),
        }
        response = client.post("/api/staff/schedules/", data)
        print("response.data:", response.data)

        assert response.status_code == 201
        assert response.data["message"] == "夜勤シフト3日分を登録しました。"
        assert len(response.data["data"]) == 3
        assert response.data["data"][0]["shift"] == "夜"
        assert response.data["data"][1]["shift"] == "明"
        assert response.data["data"][2]["shift"] == "休"

        assert WorkSchedule.objects.filter(staff=staff).count() == 3

    def test_create_schedule_with_meals(self, admin_user):
        """
        勤務シフト登録API：三食フラグ付きの登録テスト
        """
        shift = ShiftType.objects.get(code="日1")
        role, _ = Role.objects.get_or_create(name="介護士")
        staff = Staff.objects.create(name="テスト太郎", role=role, user=admin_user)

        data = {
            "staff_id": staff.id,
            "shift_id": shift.id,
            "date": str(date.today()),
            "needs_breakfast": True,
            "needs_lunch": True,
            "needs_dinner": False,
        }
        client.force_authenticate(user=admin_user)
        response = client.post("/api/staff/schedules/", data)

        assert response.status_code == 201
        assert response.data["data"]["needs_breakfast"] is True
        assert response.data["data"]["needs_lunch"] is True
        assert response.data["data"]["needs_dinner"] is False
