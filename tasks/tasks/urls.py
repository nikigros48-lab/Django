from django.contrib import admin
from django.urls import path
from tasks import views


urlpatterns = [
    path("", views.tasks, name="task_list"),
    path("<int:id>/", views.get_task, name="get_task"),
    path("longest/", views.longest_task, name="longest_task"),
    path("completed/", views.completed_tasks, name="completed_tasks"),
    path("not-completed/", views.not_completed_tasks, name="not_completed_tasks"),
    path("create/", views.create_task, name="create_task"),
    path("<int:id>/delete/", views.delete_task, name="delete_task"),
    path("<int:id>/switch-status/", views.switch_status_task, name="switch_status_task"),
    path("stats/", views.statistics, name="statistics"),
    path("delete-completed/", views.delete_completed_tasks, name="delete_completed_tasks"),
    path("search/<str:word>/", views.search_task, name="search_task"),
    path("<int:id>/edit/", views.edit_task, name="edit_task"),
    path("search/", views.search_tasks, name="search_tasks"),
]
