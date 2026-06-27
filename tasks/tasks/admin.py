from django.contrib import admin
from .models import Task, Commentary, Category, Tag, TaskDetails


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)
    ordering = ("title",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)
    ordering = ("title",)


@admin.register(TaskDetails)
class TaskDetailsAdmin(admin.ModelAdmin):
    list_display = ("task", "description", "estimated_hours")
    search_fields = ("task__title", "description")
    ordering = ("task__title",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "priority", "completed", "user", "category",)
    list_filter = ("completed", "priority", "user",)
    search_fields = ("title",)
    ordering = ("title",)


@admin.register(Commentary)
class CommentaryAdmin(admin.ModelAdmin):
    list_display = ("description", "author", "task")

