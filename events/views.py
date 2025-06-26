from rest_framework import(
    generics,permissions,
    views,serializers,
    status)
from rest_framework.response import Response

from .serializers import (
    EventSerializer,
    ListEventSerializer
)
from django_filters.rest_framework import DjangoFilterBackend
from .models import(
Event,
EventParticipant,
)
from .filters import EventFilter
from django.utils import timezone
from django.shortcuts import get_object_or_404

"""
            Event list or create APIView
"""

class EventListCreateAPIView(generics.ListCreateAPIView):
    permission_classes =  [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = EventFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ListEventSerializer
        return EventSerializer

    def get_queryset(self):
        Event.objects.filter(status='upcoming', start_date__gte=timezone.now())

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

"""
            Event join API view
"""

class EventJoinAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self,event_id):
        return get_object_or_404(Event,id=event_id)

    def post(self, request, event_id):
        event = self.get_object(event_id)

        if EventParticipant.objects.filter(user=request.user, event=event).exists():
            return Response({"error": "Already joined"}, status=400)

        if event.current_participants >= event.max_participants:
            return Response({"error": "Event is full"}, status=400)

        EventParticipant.objects.create(user=request.user, event=event)
        event.current_participants +=1
        event.save()
        return Response({"message": "Joined event"}, status=200)


"""
                Event leave API view
"""

class EventLeaveAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, event_id):
        return get_object_or_404(Event, id=event_id)

    def post(self, request, event_id):
        event = self.get_object(event_id)

        try:
            participant = EventParticipant.objects.get(user=request.user, event=event)
        except EventParticipant.DoesNotExist:
            return Response({"error": "You are not a participant"}, status=400)

        participant.delete() # leave event
        event.current_participants = max(0, event.current_participants-1) #decrease count
        event.save() #update DB

        return Response({"message": "Left event"}, status=200)

























