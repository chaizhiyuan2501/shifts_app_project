from django.db import models

class BaseModel(models.Model):
    """ベースモデル"""
    create_time=models.DateTimeField(auto_now_add=True,verbose_name="作成日時")
    update_time=models.DateTimeField(auto_now_add=True,verbose_name="更新日時")
    is_delete=models.BooleanField(default=False,verbose_name="削除フラグ")

    class Meta:
        abstract = True
        verbose_name_plural = "ベースモデル"
        db_table = "BaseTable"