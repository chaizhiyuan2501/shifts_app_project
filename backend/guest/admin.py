from django.contrib import admin
from guest.models import Guest, VisitType, VisitSchedule


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ("full_name", "birthday")
    search_fields = ("full_name",)


@admin.register(VisitType)
class VisitTypeAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "color")
    search_fields = ("code", "name")


@admin.register(VisitSchedule)
class VisitScheduleAdmin(admin.ModelAdmin):
    list_display = ("date", "guest", "visit_type", "arrive_time", "leave_time")
    list_filter = ("visit_type",)
    search_fields = ("guest__full_name",)
