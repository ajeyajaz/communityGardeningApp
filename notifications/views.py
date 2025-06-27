from  rest_framework import generics, permissions
from .serializers import  NotificationListSerializer
from .models import Notification

class NotificationListAPIView(generics.ListAPIView):
    serializer_class = NotificationListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)



