from rest_framework import generics, permissions
from .models import Comment
from .serializers import CommentSerializer

class CommentListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        event_id = self.kwargs['event_id']
        return Comment.objects.filter(event_id=event_id).order_by('-created_at')

    def perform_create(self, serializer):
        event_id = self.kwargs['event_id']
        serializer.save(user=self.request.user, event_id=event_id)




