"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tasks import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.home_page, name="home"),
    path("tasks/", views.tasks, name="task_list"),
    path("about/", views.about, name="about"),
    path("contacts/", views.contacts, name="contacts"),
    path("tasks/<int:id>/", views.get_task, name="get_task"),
    path("tasks/longest/", views.longest_task, name="longest_task"),
    path("tasks/completed/", views.completed_tasks, name="completed_tasks"),
    path("tasks/not-completed/", views.not_completed_tasks, name="not_completed_tasks"),
    path("tasks/create/", views.create_task, name="create_task"),
    path("tasks/<int:id>/delete/", views.delete_task, name="delete_task"),
    path("tasks/<int:id>/switch-status/", views.switch_status_task, name="switch_status_task"),
    path("tasks/stats/", views.statistics, name="statistics"),
    path("tasks/delete-completed/", views.delete_completed_tasks, name="delete_completed_tasks"),
    path("tasks/search/<str:word>/", views.search_task, name="search_task"),
    path("tasks/<int:id>/edit/", views.edit_task, name="edit_task"),
    path("tasks/search/", views.search_tasks, name="search_tasks"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
]
