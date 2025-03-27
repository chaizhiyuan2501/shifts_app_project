from django.contrib import admin

from .models import Guest, VisitType, VisitSchedule

# Register your models here.
admin.site.register(Guest)
admin.site.register(VisitType)
admin.site.register(VisitSchedule)
