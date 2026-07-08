from django.urls import path
from . import views


urlpatterns = [
    path('tasks/', views.TaskListCreateAPIView.as_view(), name='task_list_api'),
    path('tasks/<int:task_id>/', views.TaskAPIView.as_view(), name='task_detail_api'),
]