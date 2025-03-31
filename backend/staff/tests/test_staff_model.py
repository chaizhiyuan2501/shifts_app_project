import pytest
from datetime import time, date, timedelta

from staff.models import Staff, ShiftType, WorkSchedule, Role
from django.contrib.auth import get_user_model


@pytest.mark.django_db
class TestStaffModel:

    def setup_method(self):
        self.user = get_user_model().objects.create_user(name="testuser", password="1980")
        self.role = Role.objects.create(name="正社員")
        self.staff = Staff.objects.create(
            user=self.user, full_name="田中太郎", role=self.role
        )

        self.shift_day = ShiftType.objects.create(
            code="日", name="日勤", start_time=time(9, 0), end_time=time(18, 0)
        )
        self.shift_night = ShiftType.objects.create(
            code="夜", name="夜勤", start_time=time(17, 0), end_time=time(10, 0)
        )

    def test_monthly_work_hours_day_shift(self):
        """日勤のみでの勤務時間を計算"""
        today = date.today().replace(day=16)  # 確実に集計対象になる日
        WorkSchedule.objects.create(staff=self.staff, shift=self.shift_day, date=today)

        hours = self.staff.monthly_work_hours
        assert hours.total_seconds() == 8 * 3600  # 8時間

    def test_monthly_work_hours_night_shift(self):
        """夜勤（跨日）の勤務時間計算"""
        today = date.today().replace(day=17)
        WorkSchedule.objects.create(
            staff=self.staff, shift=self.shift_night, date=today
        )

        hours = self.staff.monthly_work_hours
        assert hours.total_seconds() == 9 * 3600  # 22:00〜翌7:00（9時間）

    def test_str_output(self):
        """__str__ が氏名を返すか"""
        assert str(self.staff) == "田中太郎"
