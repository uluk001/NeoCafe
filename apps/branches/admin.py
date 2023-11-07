from django.contrib import admin
from apps.branches.models import Branch, Schedule, Workdays

class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')


class WorkdaysAdmin(admin.ModelAdmin):
    list_display = ('schedule', 'workday', 'start_time', 'end_time')


class BranchAdmin(admin.ModelAdmin):
    list_display = ('schedule', 'address', 'phone_number', 'link_to_map')


admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Workdays, WorkdaysAdmin)
admin.site.register(Branch, BranchAdmin)