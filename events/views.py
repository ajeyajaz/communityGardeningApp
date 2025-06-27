from rest_framework import(
    generics,permissions,
    views,serializers,
    status)
from rest_framework.response import Response

from .serializers import (
    EventSerializer,
    ListEventSerializer,
    EventEditSerializer
)
from django_filters.rest_framework import DjangoFilterBackend
from .models import(
Event,
EventParticipant,
)
from .filters import EventFilter
from .permissions import IsOwnerOrReadonly
from django.utils import timezone
from django.shortcuts import get_object_or_404


"""
             Event List Or Create API View
"""
class EventListCreateAPIView(generics.ListCreateAPIView):

    permission_classes =  [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = EventFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ListEventSerializer   # return list serializer if method get
        return EventSerializer

    # return only upcoming events
    def get_queryset(self):
        Event.objects.filter(status='upcoming', start_date__gte=timezone.now())

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)


"""
              Event Join API view
"""
class EventJoinAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self,event_id):
        return get_object_or_404(Event,id=event_id)

    def post(self, request, event_id):
        event = self.get_object(event_id)

        # cannot join again if already joined
        if EventParticipant.objects.filter(user=request.user, event=event).exists():
            return Response({"error": "Already joined"}, status=400)

        # cannot join if event already full
        if event.current_participants >= event.max_participants:
            return Response({"error": "Event is full"}, status=400)

        EventParticipant.objects.create(user=request.user, event=event)
        event.current_participants +=1
        event.save()
        return Response({"message": "Joined event"}, status=200)


"""
                Event Leave API View
"""
class EventLeaveAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, event_id):
        return get_object_or_404(Event, id=event_id)

    def post(self, request, event_id):
        event = self.get_object(event_id)

        try:
            # check if user, joined before leave
            participant = EventParticipant.objects.get(user=request.user, event=event)
        except EventParticipant.DoesNotExist:
            return Response({"error": "You are not a participant"}, status=400)

        participant.delete() # leave event
        event.current_participants = max(0, event.current_participants-1) #decrease count
        event.save() #update DB

        return Response({"message": "Left event"}, status=200)


"""
                    Event Cancel API View
"""
class EventCancelAPIView(views.APIView):

    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadonly]

    def get_object(self, id):
        return get_object_or_404(Event, id=id)

    def post(self, request, id):
        event = self.get_object(id)

        self.check_object_permissions(request, event) #check user is object organizer
        if event.status in ['upcoming'] :
            event.status = "cancelled"
            event.save()
            return Response({"message": "Event cancelled"}, status=200)

        return Response({"error": "Unable perform this operation"}, status=400)


"""
                    Event Edit API
"""
class EventEditAPIView(generics.UpdateAPIView):

    queryset = Event.objects.all()
    serializer_class = EventEditSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadonly]
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        event = self.get_object()

        if event.start_date <= timezone.now(): # check if event started already
            return Response(
                {"error": "You cannot edit an event after it has started."},
                status=400
            )
        return super().update(request, *args, **kwargs)















































