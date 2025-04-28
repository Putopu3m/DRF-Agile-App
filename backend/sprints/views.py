# api/views.py
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Sprint, Pros, Cons
from .serializers import (
    SprintSerializer,
    DurationSerializer,
    ProsConsSerializer,
    ProsSerializer,
    ConsSerializer
)
from users.models import User
from rest_framework.permissions import IsAuthenticated

class SprintViewSet(ModelViewSet):
    queryset = Sprint.objects.all()
    serializer_class = SprintSerializer
    permission_classes = [IsAuthenticated]

    # GET /sprints/{id}/tasks/ - аналог getAllTasks
    @action(detail=True, methods=['get'])
    def tasks(self, request, pk=None):
        sprint = self.get_object()
        return Response({'tasks': list(sprint.tasks.values_list('id', flat=True))})

    # POST /sprints/{id}/duration/ - аналог setDuration
    @action(detail=True, methods=['post'])
    def duration(self, request, pk=None):
        sprint = self.get_object()
        serializer = DurationSerializer(data=request.data)
        if serializer.is_valid():
            sprint.duration = serializer.validated_data['duration']
            sprint.days = [0] * (sprint.duration * 7 + 1)
            sprint.save()
            return Response({'status': 'duration updated'})
        return Response(serializer.errors, status=400)

    # Pros/Cons методы
    def _handle_pros_cons(self, sprint, model, serializer_class, data):
        user = User.objects.get(id=data['user_id'])
        item = model.objects.create(user=user, text=data['name'])
        getattr(sprint, model.__name__.lower() + 's').add(item)
        return item

    # GET/POST/DELETE /sprints/{id}/pros/
    @action(detail=True, methods=['get'])
    def pros(self, request, pk=None):
        sprint = self.get_object()
        serializer = ProsSerializer(sprint.pros.all(), many=True)
        return Response(serializer.data)

    @pros.mapping.post
    def add_pros(self, request, pk=None):
        serializer = ProsConsSerializer(data=request.data)
        if serializer.is_valid():
            item = self._handle_pros_cons(self.get_object(), Pros, ProsSerializer, serializer.validated_data)
            return Response(ProsSerializer(item).data)
        return Response(serializer.errors, status=400)

    @pros.mapping.delete
    def delete_pros(self, request, pk=None):
        sprint = self.get_object()
        name = request.data.get('name')
        sprint.pros.filter(text=name).delete()
        return Response({'status': 'pros deleted'})

    # GET/POST/DELETE /sprints/{id}/cons/
    @action(detail=True, methods=['get'])
    def cons(self, request, pk=None):
        sprint = self.get_object()
        serializer = ConsSerializer(sprint.cons.all(), many=True)
        return Response(serializer.data)

    @cons.mapping.post
    def add_cons(self, request, pk=None):
        serializer = ProsConsSerializer(data=request.data)
        if serializer.is_valid():
            item = self._handle_pros_cons(self.get_object(), Cons, ConsSerializer, serializer.validated_data)
            return Response(ConsSerializer(item).data)
        return Response(serializer.errors, status=400)

    @cons.mapping.delete
    def delete_cons(self, request, pk=None):
        sprint = self.get_object()
        name = request.data.get('name')
        sprint.cons.filter(text=name).delete()
        return Response({'status': 'cons deleted'})