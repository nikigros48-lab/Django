from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('tasks/', include('tasks.urls')),
    path('', include('info.urls')),
    path('auth/', include('authorization.urls')),
    path("api/", include("tasks.api.urls")),
]
