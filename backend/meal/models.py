from django.db import models

from utils.date_utils import get_weekday_jp


class MealType(models.Model):
    """食事の種類（朝・昼・夕）"""

    name = models.CharField(
        max_length=10, unique=True, verbose_name="コード"
    )  # 例：朝、昼、夕
    display_name = models.CharField(
        max_length=20, verbose_name="表示名"
    )  # 例：朝食、昼食、夕食

    class Meta:
        verbose_name = "食事の種類"
        verbose_name_plural = "食事の種類"

    def __str__(self):
        return self.display_name


class MealOrder(models.Model):
    """1人の1食分の注文データ"""

    date = models.DateField(verbose_name="日付")
    meal_type = models.ForeignKey(
        MealType, on_delete=models.CASCADE, verbose_name="食事の種類"
    )

    guest = models.ForeignKey(
        "guest.Guest",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="患者",
    )
    staff = models.ForeignKey(
        "staff.Staff",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="スタッフ",
    )

    ordered = models.BooleanField(default=True, verbose_name="注文あり")
    auto_generated = models.BooleanField(default=True, verbose_name="自動生成")
    note = models.TextField(blank=True, null=True, verbose_name="備考")

    @property
    def weekday_jp(self):
        """
        指定した日付の曜日を日本語で返す
        """
        return get_weekday_jp(self.date)

    class Meta:
        unique_together = ("date", "meal_type", "guest", "staff")
        verbose_name = "食事の注文"
        verbose_name_plural = "食事の注文"

    def __str__(self):
        target = self.guest or self.staff
        return f"{self.date} - {target.name} - {self.meal_type.name} - {'○' if self.ordered else '×'}"
