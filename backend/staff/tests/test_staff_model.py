import pytest
from datetime import time, date, timedelta
from staff.models import Staff, ShiftType, WorkSchedule, Role
from django.contrib.auth import get_user_model


@pytest.mark.django_db
class TestStaffModel:
    """
    Staff・ShiftType モデルの単体テストクラス。
    - 勤務時間集計
    - 勤務時間計算
    - __str__ メソッド検証
    """

    def setup_method(self):
        """
        テスト用の初期データを作成
        - ユーザー
        - スタッフ
        - シフト（日勤・夜勤・夜勤明け）
        """
        self.user = get_user_model().objects.create_user(
            name="testuser", password="1980"
        )
        self.role, _ = Role.objects.get_or_create(name="正社員")
        self.staff = Staff.objects.create(
            user=self.user, name="田中太郎", role=self.role
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
        """日勤のみの勤務時間集計テスト"""
        today = date.today().replace(day=16)
        WorkSchedule.objects.create(staff=self.staff, shift=self.shift_day, date=today)

        hours = self.staff.monthly_work_hours(today)
        assert hours.total_seconds() == 8 * 3600  # 8時間

    def test_monthly_work_hours_night_shift(self):
        """
        夜勤+夜勤明けシフトの勤務時間集計テスト
        - 夜勤: 実働7時間
        - 明け: 実働10時間
        - 合計: 15時間
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
        assert hours.total_seconds() == 15 * 3600  # 15時間

    def test_get_work_duration_day_shift(self):
        """日勤シフトの実働時間計算テスト"""
        shift_day_work_hours = 8
        duration = self.shift_day.get_work_duration()
        assert duration == timedelta(hours=shift_day_work_hours)

    def test_get_work_duration_night_shift(self):
        """夜勤+夜勤明けの実働時間合計テスト"""
        shift_night_work_hours = 15
        duration = (
            self.shift_night.get_work_duration()
            + self.shift_after_night.get_work_duration()
        )

        assert duration == timedelta(hours=shift_night_work_hours)

    def test_str_output(self):
        """Staffモデルの __str__ メソッドテスト（氏名返却）"""
        assert str(self.staff) == "田中太郎"
