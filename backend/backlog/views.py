# api/views.py
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import BacklogIdea, BacklogIdeaItem
from .serializers import BacklogIdeaSerializer, BacklogIdeaItemSerializer

class BacklogIdeaViewSet(ModelViewSet):
    queryset = BacklogIdea.objects.all()
    serializer_class = BacklogIdeaSerializer

    # GET /backlog-ideas/{id}/items/ - аналог getAllBacklogIdeaItems
    @action(detail=True, methods=['get'])
    def items(self, request, pk=None):
        idea = self.get_object()
        serializer = BacklogIdeaItemSerializer(idea.items.all(), many=True)
        return Response(serializer.data)

    # POST /backlog-ideas/{id}/items/ - аналог addBacklogIdeaItem
    @action(detail=True, methods=['post'])
    def add_item(self, request, pk=None):
        idea = self.get_object()
        item = BacklogIdeaItem.objects.create(
            data=request.data.get('data'),
            priority=request.data.get('priority', 'Low')
        )
        idea.items.add(item)
        return Response(BacklogIdeaItemSerializer(item).data)

    # DELETE /backlog-ideas/{id}/items/ - аналог deleteBacklogIdeaItem
    @action(detail=True, methods=['delete'])
    def remove_item(self, request, pk=None):
        idea = self.get_object()
        item_id = request.data.get('backlog_idea_item_id')
        item = BacklogIdeaItem.objects.get(id=item_id)
        
        if item.is_tasked:
            # Логика удаления связанной задачи (аналог backlogIdeaService.js)
            pass
        
        idea.items.remove(item)
        item.delete()
        return Response({'status': 'item deleted'})
    
# api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response

class BacklogIdeaItemTaskView(APIView):
    # POST /backlog-idea-items/{id}/task/ - аналог taskBacklogIdeaItem
    def post(self, request, pk=None):
        item = BacklogIdeaItem.objects.get(id=pk)
        item.is_tasked = True
        item.save()
        return Response({'status': 'item tasked'})

    # POST /backlog-idea-items/{id}/untask/ - аналог unTaskBacklogIdeaItem
    def delete(self, request, pk=None):
        item = BacklogIdeaItem.objects.get(id=pk)
        item.is_tasked = False
        item.save()
        return Response({'status': 'item untasked'})