﻿from django.db import models
from user.models import User

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
    full_name = models.CharField(max_length=20, verbose_name="氏名")
    role = models.ForeignKey(
        Role, on_delete=models.SET_NULL, null=True, verbose_name="職種"
    )
    notes = models.TextField(blank=True, null=True, verbose_name="備考")

    class Meta:
        verbose_name = "スタッフ情報"
        verbose_name_plural = "スタッフ情報"

    def __str__(self):
        return self.full_name


class ShiftType(models.Model):
    """シフトの種類（早番、遅番、夜勤、明けなど）"""

    code = models.CharField(
        max_length=10, unique=True, verbose_name="コード"
    )  # 例：日、夜、明、休
    name = models.CharField(
        max_length=50, verbose_name="シフト名"
    )  # 例：日勤、夜勤、明け
    start_time = models.TimeField(verbose_name="開始時刻")
    end_time = models.TimeField(verbose_name="終了時刻")
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

    @property
    def monthly_work_hours(self):
        """
        現在の集計期間（15日〜翌月15日）の出勤時間合計を返す。
        """
        from .models import WorkSchedule  # 循環importを避けるためにここでインポート
        from datetime import datetime, timedelta

        # 今の集計対象期間（15日〜翌月15日）を取得
        start_date, end_date = get_shift_period_range()

        # このスタッフの出勤スケジュールを集計期間でフィルター
        schedules = WorkSchedule.objects.filter(
            staff=self, date__gte=start_date, date__lt=end_date
        )

        # 各シフトの時間を合計（開始〜終了の差分）
        total = timedelta()
        for schedule in schedules:
            shift = schedule.shift
            # 開始時間と終了時間の差分
            start_dt = datetime.combine(schedule.date, shift.start_time)
            end_dt = datetime.combine(schedule.date, shift.end_time)

            # 翌日を跨ぐ場合（例：夜勤 22:00〜翌日7:00）には1日加算
            if end_dt <= start_dt:
                end_dt += timedelta(days=1)

            total += end_dt - start_dt

        return total

    def __str__(self):
        return f"{self.code}（{self.name}）"


class WorkSchedule(models.Model):
    """勤務シフト（1人1日1件）"""

    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, verbose_name="スタッフ")
    shift = models.ForeignKey(
        ShiftType, on_delete=models.CASCADE, verbose_name="シフト"
    )
    date = models.DateField(verbose_name="日付")
    note = models.TextField(blank=True, null=True, verbose_name="備考")

    @property
    def weekday_jp(self):
        """
        指定した日付の曜日を日本語で返す
        """
        return get_weekday_jp(self.date)

    class Meta:
        # 同じスタッフが同じ日に複数のシフトに入ることを禁止する（ユニーク制約）
        unique_together = ("staff", "date")
        verbose_name = "勤務シフト"
        verbose_name_plural = "勤務シフト"

        # デフォルトの並び順：日付の昇順 → シフト（ID）の昇順で表示
        ordering = [
            "date",
            "shift",
        ]

    def __str__(self):
        return f"{self.date} - {self.staff.full_name} - {self.shift.code}"
