from django.db import models


class Guest(models.Model):
    """利用者"""
    full_name = models.CharField(max_length=50)


class Shift(models.Model):
    name = models.CharField(max_length=50)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return self.name


class Visit_Schedule(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    date = models.DateField()

    class Meta:
        ordering = [
            "date",
            "shift",
        ]  # 默认的排序方式：先按日期升序排序，再按班次升序排序
