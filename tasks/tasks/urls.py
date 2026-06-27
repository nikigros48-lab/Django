from django.urls import path
from . import views


urlpatterns = [
    path("", views.TaskListView.as_view(), name="task_list"),
    path("<int:pk>/", views.TaskDetailView.as_view(), name="get_task"),
    path("completed/", views.completed_tasks, name="completed_tasks"),
    path("not-completed/", views.not_completed_tasks, name="not_completed_tasks"),
    path("create/", views.TaskCreateView.as_view(), name="create_task"),
    path("<int:pk>/delete/", views.TaskDeleteView.as_view(), name="delete_task"),
    path("<int:id>/switch-status/", views.switch_status_task, name="switch_status_task"),
    path("stats/", views.statistics, name="statistics"),
    path("delete-completed/", views.delete_completed_tasks, name="delete_completed_tasks"),
    path("search/<str:word>/", views.search_task, name="search_task"),
    path("<int:pk>/edit/", views.TaskUpdateView.as_view(), name="edit_task"),
    path("search/", views.search_tasks, name="search_tasks"),
    path("categories/", views.CategoryListView.as_view(), name="get_all_categories"),
    path("categories/<int:pk>/", views.CategoryDetailView.as_view(), name="get_category_tasks"),
    path("tags/<int:pk>/", views.TagDetailView.as_view(), name="task_tags"),
]
