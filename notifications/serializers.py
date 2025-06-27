from rest_framework import serializers
from .models import Notification


class NotificationListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = ['id', 'message', 'is_read', 'created_at']


