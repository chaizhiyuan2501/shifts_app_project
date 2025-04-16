from django.db import models
from user.models import User
from datetime import datetime, timedelta, date

from utils.date_utils import get_weekday_jp, get_shift_period_range


class Role(models.Model):
    """職種（正社員、アルバイト、夜勤専門 など）"""

    name = models.CharField(max_length=255, unique=True, verbose_name="職種名")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "職種"
        verbose_name_plural = "職種"


class Staff(models.Model):
    """スタッフ情報"""

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
        現在の集計期間（15日〜翌月15日）の出勤時間合計を返す（休憩時間を除く）。

        使用例:
            staff = Staff.objects.get(name="田中太郎")
            print(staff.monthly_work_hours())  # 例: 2 days, 6:00:00

        パラメータ:
            target_date: 任意指定された日付（例：2025-04-01）→ 属する15日-翌15日の範囲で集計

        戻り値:
            datetime.timedelta 型の合計時間（休憩時間を引いた実働時間）
        """
        from .models import WorkSchedule
        from datetime import datetime, timedelta

        start_date, end_date = get_shift_period_range(target_date)
        schedules = WorkSchedule.objects.filter(
            staff=self, date__gte=start_date, date__lt=end_date
        )

        total = timedelta()
        for schedule in schedules:
            shift = schedule.shift
            start_dt = datetime.combine(schedule.date, shift.start_time)
            end_dt = datetime.combine(schedule.date, shift.end_time)

            # 翌日にまたがる場合（夜勤など）
            if end_dt <= start_dt:
                end_dt += timedelta(days=1)

            work_duration = end_dt - start_dt
            break_duration = timedelta(minutes=shift.break_minutes or 0)

            total += work_duration - break_duration

        return total


class ShiftType(models.Model):
    """シフトの種類（早番、遅番、夜勤、明けなど）"""

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
        実際の勤務時間（休憩時間を引いた時間）を timedelta で返す。
        """
        today = datetime.today().date()
        start_dt = datetime.combine(today, self.start_time)
        end_dt = datetime.combine(today, self.end_time)

        # end が start より早ければ、翌日の勤務とみなす
        if end_dt <= start_dt:
            end_dt += timedelta(days=1)

        duration = end_dt - start_dt - timedelta(minutes=self.break_minutes)
        return duration


class WorkSchedule(models.Model):
    """勤務シフト（1人1日1件）"""

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
        指定した日付の曜日を日本語で返す
        """
        return get_weekday_jp(self.date)
