from django.contrib import admin
from .models import Role, Staff, ShiftType, WorkSchedule


admin.site.register(Role)
admin.site.register(Staff)
admin.site.register(WorkSchedule)
admin.site.register(ShiftType)


class ShiftTypeAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "name",
        "start_time",
        "end_time",
        "break_minutes",
        "get_work_hours",
    )

    def get_work_hours(self, obj):
        # 時間（timedelta）を float に変換（例：8.75時間）
        duration = obj.get_work_duration()
        return round(duration.total_seconds() / 3600, 2)

    get_work_hours.short_description = "勤務時間（h）"
