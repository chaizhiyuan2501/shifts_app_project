from django.db import models
from datetime import time


class Date(models.Model):
    date = models.DateField()

    def strf_date(self):
        return self.date.strftime("%Y/%m/%d, %a")

    class Meta:
        abstract = True


class TimeTable(models.Model):
    start = models.TimeField(default=time(0, 0))  # 默认值修正
    end = models.TimeField(default=time(0, 0))  # 默认值修正

    def strftimetable(self) -> str:
        timef = "%H:%M"
        if self.start and self.end:  # 确保 start 和 end 有值
            return f"{self.start.strftime(timef)} ~ {self.end.strftime(timef)}"
        return "Invalid Time"

    class Meta:
        abstract = True


class BaseModel(models.Model):
    """ベースモデル"""

    create_date_time = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    update_date_time = models.DateTimeField(auto_now_add=True, verbose_name="更新日時")
    is_deleted = models.BooleanField(default=False, verbose_name="削除フラグ")

    class Meta:
        abstract = True
        verbose_name_plural = "ベースモデル"
        db_table = "BaseTable"
