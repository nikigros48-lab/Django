from django.urls import path
from . import views


urlpatterns = [
    path('tasks/', views.task_list, name='task_list_api'),
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail_api'),
]