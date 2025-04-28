# api/views.py
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer, MessageCreateSerializer
from users.models import User
from rest_framework.permissions import IsAuthenticated

class ConversationViewSet(ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    # GET /conversations/{id}/messages/ - аналог getAllMessages
    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        conversation = self.get_object()
        serializer = MessageSerializer(conversation.messages.all(), many=True)
        return Response(serializer.data)

    # POST /conversations/{id}/messages/ - аналог addMessage
    @action(detail=True, methods=['post'])
    def add_message(self, request, pk=None):
        conversation = self.get_object()
        serializer = MessageCreateSerializer(data=request.data)
        
        if serializer.is_valid():
            sender = User.objects.get(id=serializer.validated_data['sender_id'])
            message = Message.objects.create(
                text=serializer.validated_data['text'],
                sender=sender
            )
            conversation.messages.add(message)
            return Response(MessageSerializer(message).data)
        
        return Response(serializer.errors, status=400)

    # DELETE /conversations/{id}/messages/ - аналог deleteMessage
    @action(detail=True, methods=['delete'])
    def delete_message(self, request, pk=None):
        conversation = self.get_object()
        message_id = request.data.get('message_id')
        message = Message.objects.get(id=message_id)
        
        conversation.messages.remove(message)
        message.delete()
        return Response({'status': 'message deleted'})