from django.db import models
from django.contrib.auth.models import User


class Role(models.Model):
    """护工角色定义"""

    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Staff(models.Model):
    """スタッフ"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="")
    full_name = models.CharField(max_length=20)
    role = models.ForeignKey(Role, on_delete=models.models.SET_NULL, null=True)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name


class Shift(models.Model):
    name = models.CharField(max_length=50)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return self.name


class WorkSchedule(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    date = models.DateField()

    class Meta:
        unique_together = ("staff", "date")  # 同一人同一天只能排一个班
        ordering = [
            "date",
            "shift",
        ]  # 默认的排序方式：先按日期升序排序，再按班次升序排序
