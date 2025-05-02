from django.db import models
from user.models import User
from datetime import datetime, timedelta, date

from utils.date_utils import get_weekday_jp, get_shift_period_range
from utils.model_utils import BaseNeedMeal


class Role(models.Model):
    """職種モデル（正社員、アルバイト、夜勤専門など）を管理する"""

    name = models.CharField(max_length=255, unique=True, verbose_name="職種名")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "職種"
        verbose_name_plural = "職種"


class Staff(models.Model):
    """スタッフ基本情報モデル"""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="ユーザー",
        related_name="staff_profile",
    )
    name = models.CharField(max_length=20, verbose_name="氏名")
    role = models.ForeignKey(
        Role, on_delete=models.SET_NULL, null=True, verbose_name="職種"
    )
    notes = models.TextField(blank=True, null=True, verbose_name="備考")

    class Meta:
        verbose_name = "スタッフ情報"
        verbose_name_plural = "スタッフ情報"

    def __str__(self):
        return self.name

    def monthly_work_hours(self, target_date=None):
        """
        指定された月の出勤実働時間（休憩時間を除く）を集計して返す。

        Args:
            target_date (datetime.date, optional): 任意の日付。指定がなければ今日。

        Returns:
            datetime.timedelta: 合計実働時間
        """
        from .models import WorkSchedule

        start_date, end_date = get_shift_period_range(target_date)
        schedules = WorkSchedule.objects.filter(
            staff=self, date__gte=start_date, date__lt=end_date
        )

        total = timedelta()
        for schedule in schedules:
            shift = schedule.shift
            start_dt = datetime.combine(schedule.date, shift.start_time)
            end_dt = datetime.combine(schedule.date, shift.end_time)

            # 夜勤など翌日跨りの場合対応
            if end_dt <= start_dt:
                end_dt += timedelta(days=1)

            work_duration = end_dt - start_dt
            break_duration = timedelta(minutes=shift.break_minutes or 0)

            total += work_duration - break_duration

        return total


class ShiftType(models.Model):
    """シフト種類モデル（早番、遅番、夜勤など）"""

    code = models.CharField(max_length=10, unique=True, verbose_name="コード")
    name = models.CharField(max_length=50, verbose_name="シフト名")
    start_time = models.TimeField(verbose_name="開始時刻")
    end_time = models.TimeField(verbose_name="終了時刻")
    break_minutes = models.PositiveIntegerField(default=0, verbose_name="休憩時間(分)")
    color = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        default="#00000",
        verbose_name="表示色（オプション）",
    )

    class Meta:
        verbose_name = "シフトの種類"
        verbose_name_plural = "シフトの種類"

    def __str__(self):
        return f"{self.code}（{self.name}）"

    def get_work_duration(self):
        """
        勤務時間（休憩時間差引後）をtimedeltaで取得する。

        Returns:
            datetime.timedelta: 実働時間
        """
        today = datetime.today().date()
        start_dt = datetime.combine(today, self.start_time)
        end_dt = datetime.combine(today, self.end_time)

        if end_dt <= start_dt:
            end_dt += timedelta(days=1)

        duration = end_dt - start_dt - timedelta(minutes=self.break_minutes)
        return duration


class WorkSchedule(BaseNeedMeal,models.Model):
    """勤務シフト管理モデル（スタッフ毎・日毎のシフト情報）"""

    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, verbose_name="スタッフ")
    shift = models.ForeignKey(
        ShiftType, on_delete=models.CASCADE, verbose_name="シフト"
    )
    date = models.DateField(verbose_name="日付")
    note = models.TextField(blank=True, null=True, verbose_name="備考")

    class Meta:
        unique_together = ("staff", "date")
        verbose_name = "勤務シフト"
        verbose_name_plural = "勤務シフト"
        ordering = ["date", "shift"]

    def __str__(self):
        return f"{self.date} - {self.staff.name} - {self.shift.code}"

    @property
    def weekday_jp(self):
        """
        勤務日の曜日を日本語で取得する。

        Returns:
            str: 日本語の曜日名（例：月、火、水）
        """
        return get_weekday_jp(self.date)
