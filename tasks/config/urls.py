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
    path("", views.home_page),
    path("tasks/", views.tasks),
    path("about/", views.about),
    path("user/<int:id>/", views.user_detail),
    path("contacts/", views.contacts),
    path("hello/<str:name>/", views.hello),
    path("number/<int:num>/", views.number),
    path("sum/<int:num1>/<int:num2>/", views.sum),
    path("maximum/<int:num1>/<int:num2>/", views.maximum),
    path("tasks/<int:index>/", views.get_task),
    path("tasks/longest/", views.tasks_long),
]
