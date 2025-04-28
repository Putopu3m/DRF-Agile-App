# api/views.py
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Team
from .serializers import TeamSerializer, TeamUserActionSerializer
from users.models import User
from rest_framework.permissions import IsAuthenticated

class TeamViewSet(ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]  # Требуем JWT

    # GET /teams/{id}/ - аналог getTeam
    # POST /teams/ - создание (автоматически от DRF)

    # GET /teams/{id}/users/ - аналог getAllTeamUsers
    @action(detail=True, methods=['get'])
    def users(self, request, pk=None):
        team = self.get_object()
        serializer = UserSerializer(team.users.all(), many=True)
        return Response(serializer.data)

    # POST /teams/{id}/users/ - аналог addTeamUser
    @action(detail=True, methods=['post'])
    def add_user(self, request, pk=None):
        team = self.get_object()
        serializer = TeamUserActionSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(id=serializer.validated_data['user_id'])
            team.users.add(user)
            user.teams.add(team)  # Обновляем связь с User
            return Response({'status': 'user added'})
        return Response(serializer.errors, status=400)

    # DELETE /teams/{id}/users/ - аналог deleteTeamUser
    @action(detail=True, methods=['delete'])
    def remove_user(self, request, pk=None):
        team = self.get_object()
        serializer = TeamUserActionSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(id=serializer.validated_data['user_id'])
            team.users.remove(user)
            user.teams.remove(team)  # Обновляем связь с User
            return Response({'status': 'user removed'})
        return Response(serializer.errors, status=400)