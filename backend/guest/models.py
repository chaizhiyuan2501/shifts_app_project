from django.db import models


class Guest(models.Model):
    """利用者情報"""

    full_name = models.CharField(max_length=50, verbose_name="氏名")
    birthday = models.DateField(null=True, blank=True, verbose_name="生年月日")
    contact = models.CharField(max_length=100, blank=True, verbose_name="連絡先")

    def __str__(self):
        return self.full_name


class VisitType(models.Model):
    """来訪種別（泊、通い、休み など）"""

    code = models.CharField(
        max_length=10, unique=True, verbose_name="コード"
    )  # 例：泊、通い、休
    name = models.CharField(
        max_length=50, verbose_name="表示名"
    )  # 例：泊まり、通い、休み
    arrive_time = models.TimeField(verbose_name="来所時間")
    leave_time = models.TimeField(verbose_name="帰宅時間")
    color = models.CharField(max_length=10, default="#cccccc", verbose_name="色コード")

    def __str__(self):
        return f"{self.code}（{self.name}）"


class VisitSchedule(models.Model):
    """患者の来訪スケジュール（1人1日1件）"""

    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, verbose_name="利用者")
    date = models.DateField(verbose_name="日付")
    visit_type = models.ForeignKey(
        VisitType, on_delete=models.SET_NULL, null=True, verbose_name="来訪種別"
    )
    note = models.TextField(blank=True, null=True, verbose_name="備考")

    class Meta:
        unique_together = ("guest", "date")
        ordering = ["date"]

    def __str__(self):
        return f"{self.date} - {self.guest.full_name} - {self.visit_type.code if self.visit_type else '未定'}"
