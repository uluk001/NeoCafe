from django.contrib import admin

from apps.branches.models import Branch, Schedule, Workdays


class WorkdaysInline(admin.TabularInline):
    model = Workdays
    extra = 1


class ScheduleAdmin(admin.ModelAdmin):
    list_display = ("title",)
    inlines = [WorkdaysInline]


class BranchAdmin(admin.ModelAdmin):
    list_display = ("address", "phone_number", "schedule", "link_to_map", "counts_of_tables")


admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Branch, BranchAdmin)
