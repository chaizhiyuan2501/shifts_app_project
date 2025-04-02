﻿import pytest
from datetime import time, date, timedelta
from staff.models import Staff, ShiftType, WorkSchedule, Role
from django.contrib.auth import get_user_model


@pytest.mark.django_db
class TestStaffModel:
    """
    Staff・ShiftTypeモデルに関するテストクラス。
    勤務時間の計算やプロパティの動作確認などを行う。
    """

    def setup_method(self):
        self.user = get_user_model().objects.create_user(
            name="testuser", password="1980"
        )
        self.role, _ = Role.objects.get_or_create(name="正社員")
        self.staff = Staff.objects.create(
            user=self.user, full_name="田中太郎", role=self.role
        )

        self.shift_day, _ = ShiftType.objects.get_or_create(
            code="日",
            defaults={
                "name": "日勤",
                "start_time": time(9, 0),
                "end_time": time(18, 0),
                "break_minutes": 60,
                "color": "#00000",
            },
        )
        self.shift_night, _ = ShiftType.objects.get_or_create(
            code="夜",
            defaults={
                "name": "夜勤",
                "start_time": time(17, 0),
                "end_time": time(0, 0),
                "break_minutes": 60,
                "color": "#00000",
            },
        )
        self.shift_after_night, _ = ShiftType.objects.get_or_create(
            code="明",
            defaults={
                "name": "夜勤明け",
                "start_time": time(0, 0),
                "end_time": time(10, 0),
                "break_minutes": 60,
                "color": "#00000",
            },
        )

    def test_monthly_work_hours_day_shift(self):
        """日勤のみでの勤務時間を計算"""
        today = date.today().replace(day=16)
        WorkSchedule.objects.create(staff=self.staff, shift=self.shift_day, date=today)

        hours = self.staff.monthly_work_hours(today)
        assert hours.total_seconds() == 8 * 3600  # 8時間

    def test_monthly_work_hours_night_shift(self):
        """
        夜勤と夜勤明けの連続勤務時間を計算
        - 夜勤: 17:00〜翌0:00（7時間、休憩1時間）
        - 明け: 翌0:00〜10:00（10時間、休憩1時間）
        - 合計: 7+10 - 1-1 = 実働15時間
        """
        today = date.today().replace(day=17)
        WorkSchedule.objects.create(
            staff=self.staff, shift=self.shift_night, date=today
        )
        WorkSchedule.objects.create(
            staff=self.staff,
            shift=self.shift_after_night,
            date=today + timedelta(days=1),
        )
        hours = self.staff.monthly_work_hours(today)
        assert hours.total_seconds() == 15 * 3600  # 実働17時間 - 休憩2時間

    def test_get_work_duration_day_shift(self):
        """日勤の実働時間が正しく計算されるか（休憩1時間）"""
        shift_day_work_hours = 8
        duration = self.shift_day.get_work_duration()
        assert duration == timedelta(hours=shift_day_work_hours)

    def test_get_work_duration_night_shift(self):
        """夜勤の実働時間が正しく計算されるか（休憩2時間）"""
        shift_night_work_hours = 15
        duration = (
            self.shift_night.get_work_duration()
            + self.shift_after_night.get_work_duration()
        )

        assert duration == timedelta(hours=shift_night_work_hours)

    def test_str_output(self):
        """__str__ が氏名を返すか"""
        assert str(self.staff) == "田中太郎"
