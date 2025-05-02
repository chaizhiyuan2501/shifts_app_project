from django.db import models


class BaseModel(models.Model):
    """ベースモデル"""

    create_time = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    update_time = models.DateTimeField(auto_now_add=True, verbose_name="更新日時")
    is_delete = models.BooleanField(default=False, verbose_name="削除フラグ")

    class Meta:
        abstract = True
        verbose_name_plural = "ベースモデル"
        db_table = "BaseTable"


class BaseNeedMeal(models.Model):
    needs_breakfast = models.BooleanField(default=False, verbose_name="朝食要るか")
    needs_lunch = models.BooleanField(default=False, verbose_name="昼食要るか")
    needs_dinner = models.BooleanField(default=False, verbose_name="夕食要るか")
    meal_note = models.TextField(blank=True, null=True, verbose_name="食事に関する備考")

    class Meta:
        abstract = True
        verbose_name = "食事の要否設定"
        verbose_name_plural = "食事の要否設定"
