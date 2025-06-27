from rest_framework.test import APITestCase
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from users.models import User
from events.models import Event, EventParticipant
from notifications.models import Notification
from rest_framework_simplejwt.tokens import RefreshToken

class NotificationListAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='ajay', email='ajay@gmail.com', password='testpass123')
        self.other_user = User.objects.create_user(username='guest', email='guest@gmail.com', password='guestpass')

        self.event = Event.objects.create(
            title='Clean Up Drive',
            description='Let’s clean the park!',
            start_date=timezone.now() + timedelta(days=2),
            end_date=timezone.now() + timedelta(days=2, hours=2),
            location_name='Eco Park',
            min_participants=2,
            max_participants=15,
            organizer=self.user
        )

        # Create notifications for both users
        Notification.objects.create(user=self.user, message='New comment on your event.')
        Notification.objects.create(user=self.other_user, message='Event you joined has been updated.')

        # Auth setup
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

    def test_authenticated_user_sees_only_their_notifications(self):
        response = self.client.get('/api/notifications/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        for notif in response.data:
            self.assertTrue(
                'New comment' in notif['message'] or 'Event you joined' in notif['message']
            )

    def test_unauthenticated_user_cannot_access_notifications(self):
        self.client.credentials()  # Remove auth
        response = self.client.get('/api/notifications/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


