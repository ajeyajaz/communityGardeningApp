from django.urls import path
from .views import (
EventListCreateAPIView,
EventJoinAPIView,
EventLeaveAPIView
)

urlpatterns = [

    path('',EventListCreateAPIView.as_view() ,name='event-create-list-api'),

    path('<int:event_id>/join/', EventJoinAPIView.as_view(), name='event-join-api'),
    path('<int:event_id>/leave/', EventLeaveAPIView.as_view(), name='event-leave-api'),
]


