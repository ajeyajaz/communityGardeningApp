from rest_framework.test import APITestCase, APIClient
from users.models import User
from django.utils import timezone
from datetime import timedelta
from events.models import Event,EventParticipant
from rest_framework_simplejwt.tokens import RefreshToken



"""
                Event join/leave Test cases
"""

class EventParticipationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='ajay', email='ajay@example.com', password='testpass123')
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(refresh.access_token))

        self.event = Event.objects.create(
            title='Green Clean',
            description='Gardening Event',
            start_date=timezone.now() + timedelta(days=1),
            end_date=timezone.now() + timedelta(days=1, hours=2),
            location_name='Park',
            min_participants=1,
            max_participants=2,
            current_participants=0,
            organizer=self.user,
        )

        self.url_join = f'/api/events/{self.event.id}/join/'
        self.url_leave = f'/api/events/{self.event.id}/leave/'

    def test_user_can_join_event(self):
        response = self.client.post(self.url_join)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(EventParticipant.objects.count(), 1)
        self.assertEqual(EventParticipant.objects.first().user, self.user)

    def test_user_cannot_join_twice(self):
        EventParticipant.objects.create(user=self.user, event=self.event)
        self.event.current_participants = 1
        self.event.save()

        response = self.client.post(self.url_join)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Already joined", response.data["error"])

    def test_user_cannot_join_full_event(self):
        # Fill the event
        user2 = User.objects.create_user(username='other', email='other@example.com', password='pass')
        EventParticipant.objects.create(user=self.user, event=self.event)
        EventParticipant.objects.create(user=user2, event=self.event)
        self.event.current_participants = 2
        self.event.save()

        user3 = User.objects.create_user(username='third', email='third@example.com', password='pass')
        refresh = RefreshToken.for_user(user3)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(refresh.access_token))

        response = self.client.post(self.url_join)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Event is full", response.data["error"])

    def test_user_can_leave_event(self):
        EventParticipant.objects.create(user=self.user, event=self.event)
        self.event.current_participants = 1
        self.event.save()

        response = self.client.post(self.url_leave)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(EventParticipant.objects.count(), 0)
        self.event.refresh_from_db()
        self.assertEqual(self.event.current_participants, 0)

    def test_user_cannot_leave_if_not_participant(self):
        response = self.client.post(self.url_leave)
        self.assertEqual(response.status_code, 400)
        self.assertIn("not a participant", response.data["error"])
