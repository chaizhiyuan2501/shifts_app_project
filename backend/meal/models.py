from django.db import models


class MealType(models.Model):
    """食事の種類（朝・昼・夕）"""

    name = models.CharField(
        max_length=10, unique=True, verbose_name="コード"
    )  # 例：朝、昼、夕
    display_name = models.CharField(
        max_length=20, verbose_name="表示名"
    )  # 例：朝食、昼食、夕食

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

    class Meta:
        unique_together = ("date", "meal_type", "guest", "staff")

    def __str__(self):
        target = self.guest or self.staff
        return f"{self.date} - {target.full_name} - {self.meal_type.name} - {'○' if self.ordered else '×'}"
