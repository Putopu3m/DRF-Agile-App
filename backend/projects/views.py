# api/views.py
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Project, Task
from .serializers import ProjectSerializer

class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    # Автоматически доступны: GET /projects/, POST /projects/, PUT /projects/1/, DELETE /projects/1/

    # Кастомные методы (аналог projectService.js)
    @action(detail=True, methods=['post'])
    def add_task(self, request, pk=None):
        project = self.get_object()
        task = Task.objects.create(
            name=request.data.get('name'),
            priority=request.data.get('priority', 'Low'),
            project=project
        )
        return Response({'id': task.id})

    @action(detail=True, methods=['get'])
    def backlog_ideas(self, request, pk=None):
        project = self.get_object()
        ideas = []  # Замените на реальные данные из BacklogIdea
        return Response(ideas)

    # Аналог changeAccess
    @action(detail=True, methods=['post'])
    def change_access(self, request, pk=None):
        project = self.get_object()
        project.is_private = request.data.get('state')
        project.save()
        return Response({'status': 'success'})