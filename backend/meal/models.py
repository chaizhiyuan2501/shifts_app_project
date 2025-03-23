from django.db import models


class MealType(models.Model):
    """食事の種類（朝・昼・夕）"""
    name = models.CharField("コード", max_length=10, unique=True)  # 例：朝、昼、夕
    display_name = models.CharField("表示名", max_length=20)       # 例：朝食、昼食、夕食

    def __str__(self):
        return self.display_name


class MealOrder(models.Model):
    """1人の1食分の注文データ"""

    date = models.DateField("日付")
    meal_type = models.ForeignKey(MealType, on_delete=models.CASCADE)

    guest = models.ForeignKey(
        "guest.Guest", on_delete=models.CASCADE, null=True, blank=True, verbose_name="患者"
    )
    staff = models.ForeignKey(
        "staff.Staff", on_delete=models.CASCADE, null=True, blank=True, verbose_name="スタッフ"
    )

    ordered = models.BooleanField("注文あり", default=True)
    auto_generated = models.BooleanField("自動生成", default=True)
    note = models.TextField("備考", blank=True, null=True)

    class Meta:
        unique_together = ("date", "meal_type", "guest", "staff")

    def __str__(self):
        target = self.guest or self.staff
        return f"{self.date} - {target.full_name} - {self.meal_type.name} - {'○' if self.ordered else '×'}"
