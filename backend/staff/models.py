from django.db import models
from django.contrib.auth.models import User


class Role(models.Model):
    """職種（正社員、アルバイト、夜勤専門 など）"""

    name = models.CharField("職種名", max_length=255, unique=True)

    def __str__(self):
        return self.name


class Staff(models.Model):
    """スタッフ情報"""

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="ユーザーアカウント"
    )
    full_name = models.CharField(max_length=20, verbose_name="氏名")
    role = models.ForeignKey(
        Role, on_delete=models.SET_NULL, null=True, verbose_name="職種"
    )
    is_admin = models.BooleanField(default=False, verbose_name="管理者権限")

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

    class Meta:
        # 同じスタッフが同じ日に複数のシフトに入ることを禁止する（ユニーク制約）
        unique_together = ("staff", "date")

        # デフォルトの並び順：日付の昇順 → シフト（ID）の昇順で表示
        ordering = [
            "date",
            "shift",
        ]

    def __str__(self):
        return f"{self.date} - {self.staff.full_name} - {self.shift.code}"
