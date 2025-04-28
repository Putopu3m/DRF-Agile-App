# api/urls.py
from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import BacklogIdeaViewSet, BacklogIdeaItemTaskView

router = DefaultRouter()
router.register(r'backlog-ideas', BacklogIdeaViewSet, basename='backlogidea')

urlpatterns = [
    path('backlog-idea-items/<int:pk>/task/', BacklogIdeaItemTaskView.as_view(), name='task-item'),
    path('backlog-idea-items/<int:pk>/untask/', BacklogIdeaItemTaskView.as_view(), name='untask-item'),
] + router.urls