from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "priority", "completed", "user", "category__title", "tags__title")
    list_filter = ("completed", "priority", "user", "category__title", "tags__title")
    search_fields = ("title",)
    ordering = ("title",)
    


