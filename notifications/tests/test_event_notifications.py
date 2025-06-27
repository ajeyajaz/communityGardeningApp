from rest_framework.test import APITestCase
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from users.models import User
from events.models import Event, EventParticipant
from notifications.models import Notification

class EventNotificationSignalTests(APITestCase):
    def setUp(self):
        self.organizer = User.objects.create_user(username='organizer', email='org@gmail.com', password='pass1234')
        self.participant = User.objects.create_user(username='participant', email='part@gmail.com', password='pass1234')

        self.event = Event.objects.create(
            title='Park Cleanup',
            description='Help clean the community park',
            start_date=timezone.now() + timedelta(days=1),
            end_date=timezone.now() + timedelta(days=1, hours=2),
            location_name='Eco Park',
            min_participants=1,
            max_participants=10,
            organizer=self.organizer
        )

    def test_notification_created_on_join(self):
        # Participant joins event
        EventParticipant.objects.create(user=self.participant, event=self.event)

        # Organizer should receive notification
        notification = Notification.objects.filter(user=self.organizer).first()
        self.assertIsNotNone(notification)
        self.assertIn("joined your event", notification.message)

    def test_notification_created_on_leave(self):
        # First join
        participant_record = EventParticipant.objects.create(user=self.participant, event=self.event)
        Notification.objects.all().delete()  # Clear the "join" notification

        # Then leave
        participant_record.delete()

        # Organizer should receive "left" notification
        notification = Notification.objects.filter(user=self.organizer).first()
        self.assertIsNotNone(notification)
        self.assertIn("left your event", notification.message)
