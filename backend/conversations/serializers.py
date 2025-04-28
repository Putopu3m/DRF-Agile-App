# api/serializers.py
from rest_framework import serializers
from .models import Conversation, Message
from users.serializers import UserSerializer

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'text', 'sender', 'created_at']

class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    creator = UserSerializer(read_only=True)

    class Meta:
        model = Conversation
        fields = ['id', 'name', 'creator', 'messages', 'created_at']

class MessageCreateSerializer(serializers.Serializer):
    text = serializers.CharField()
    sender_id = serializers.IntegerField()