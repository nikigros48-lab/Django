from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "priority", "completed")
    list_filter = ("completed", "priority")
    search_fields = ("title",)
    ordering = ("title", "priority")
    


