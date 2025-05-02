from django.db import models

from utils.model_utils import BaseNeedMeal
from utils.date_utils import get_weekday_jp


class Guest(models.Model):
    """
    利用者情報モデル
    - 氏名、生年月日、連絡先、備考を保持
    """

    name = models.CharField(max_length=50, verbose_name="氏名")
    birthday = models.DateField(null=True, blank=True, verbose_name="生年月日")
    contact = models.CharField(max_length=100, blank=True, verbose_name="連絡先")
    notes = models.TextField(blank=True, null=True, verbose_name="備考")

    class Meta:
        verbose_name = "利用者情報"
        verbose_name_plural = "利用者情報"

    def __str__(self):
        return self.name


class VisitType(models.Model):
    """
    来訪種別モデル（泊・通い・休みなど）
    - コード（例: 泊）とその日本語表記・色を管理
    """

    code = models.CharField(max_length=10, unique=True, verbose_name="コード")
    name = models.CharField(max_length=50, verbose_name="来訪種別")
    color = models.CharField(max_length=10, default="#cccccc", verbose_name="色コード")

    class Meta:
        verbose_name = "来訪種別"
        verbose_name_plural = "来訪種別"

    def __str__(self):
        return f"{self.code}（{self.name}）"


class VisitSchedule(BaseNeedMeal, models.Model):
    """
    来訪スケジュールモデル
    - 利用者と日付のユニーク制約あり（1人1日1件）
    - 来所時間と帰宅時間も保持
    """

    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, verbose_name="利用者")
    visit_type = models.ForeignKey(
        VisitType, on_delete=models.SET_NULL, null=True, verbose_name="来訪種別"
    )
    date = models.DateField(verbose_name="日付")
    arrive_time = models.TimeField(verbose_name="来所時間", null=True)
    leave_time = models.TimeField(verbose_name="帰宅時間", null=True)
    note = models.TextField(blank=True, null=True, verbose_name="備考")

    @property
    def weekday_jp(self):
        """
        日付の曜日（日本語）を返す
        """
        return get_weekday_jp(self.date)

    class Meta:
        unique_together = ("guest", "date")  # 同じ利用者・同日で重複不可
        ordering = ["date"]
        verbose_name = "来訪スケジュール"
        verbose_name_plural = "来訪スケジュール"

    def __str__(self):
        return f"{self.date} - {self.guest.name} - {self.visit_type.code if self.visit_type else '未定'}"
