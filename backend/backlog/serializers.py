# api/serializers.py
from rest_framework import serializers
from .models import BacklogIdea, BacklogIdeaItem

class BacklogIdeaItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BacklogIdeaItem
        fields = ['id', 'priority', 'data', 'is_tasked', 'created_at']

class BacklogIdeaSerializer(serializers.ModelSerializer):
    items = BacklogIdeaItemSerializer(many=True, read_only=True)

    class Meta:
        model = BacklogIdea
        fields = ['id', 'name', 'items', 'sprint', 'created_at']

class TaskActionSerializer(serializers.Serializer):
    backlog_idea_item_id = serializers.IntegerField()