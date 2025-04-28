from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('projects/', include('projects.urls')),
    path('sprints/', include('sprints.urls')),
    path('backlog/', include('backlog.urls')),
    path('conversations/', include('conversations.urls')),
]
