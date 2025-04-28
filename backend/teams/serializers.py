# api/serializers.py
from rest_framework import serializers
from .models import Team
from users.serializers import UserSerializer

class TeamSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)
    
    class Meta:
        model = Team
        fields = ['id', 'name', 'users', 'creator', 'created_at']
        read_only_fields = ['creator']

class TeamUserActionSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()