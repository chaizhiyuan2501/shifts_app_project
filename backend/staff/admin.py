from django.contrib import admin
from .models import Role, Staff, ShiftType, WorkSchedule


admin.site.register(Role)
admin.site.register(Staff)
admin.site.register(ShiftType)
admin.site.register(WorkSchedule)
