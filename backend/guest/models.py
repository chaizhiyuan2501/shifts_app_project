from django.db import models


class Guest(models.Model):
    """利用者情報"""
    full_name = models.CharField(max_length=50)
    birthday  = models.DateField(null=True,blank=True)
    contact = models.CharField(max_length=100,blank=True)

    def __str__(self):
        return self.full_name


class VisitType(models.Model):
    """来訪種別（泊、通い、休み など）"""
    code = models.CharField("コード", max_length=10, unique=True)  # 例：泊、通い、休
    name = models.CharField("表示名", max_length=50)  # 例：泊まり、通い、休み
    arrive_time = models.TimeField(verbose_name="来所時間")
    leave_time = models.TimeField(verbose_name="帰宅時間")
    color = models.CharField("色コード", max_length=10, default="#cccccc")

    def __str__(self):
        return f"{self.code}（{self.name}）"


class GuestVisitSchedule(models.Model):
    """患者の来訪スケジュール（1人1日1件）"""

    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, verbose_name="利用者")
    date = models.DateField("日付")
    visit_type = models.ForeignKey(VisitType, on_delete=models.SET_NULL, null=True, verbose_name="来訪種別")
    note = models.TextField("備考", blank=True, null=True)

    class Meta:
        unique_together = ("guest", "date")
        ordering = ["date"]

    def __str__(self):
        return f"{self.date} - {self.guest.full_name} - {self.visit_type.code if self.visit_type else '未定'}"