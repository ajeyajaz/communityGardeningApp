from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from users.models import User
from events.models import Event

class EventEditCancelPermissionTests(APITestCase):
    def setUp(self):
        self.creator = User.objects.create_user(username="ajay", email='ajey@example.com',password="test123")
        self.other_user = User.objects.create_user(username="not_ajay", password="test123")

        self.event = Event.objects.create(
            title="Community Planting",
            description="Plant trees in the park",
            location_name="City Park",
            start_date=timezone.now() + timedelta(days=2),
            end_date=timezone.now() + timedelta(days=2, hours=2),
            max_participants=20,
            organizer=self.creator
        )

        self.edit_url = f"/api/events/{self.event.id}/edit/"
        self.cancel_url = f"/api/events/{self.event.id}/cancel/"

    def get_auth_client(self, user):
        client = APIClient()
        client.force_authenticate(user=user)
        return client

    def test_creator_can_edit_event(self):
        client = self.get_auth_client(self.creator)
        response = client.patch(self.edit_url, {"title": "Updated Event"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.event.refresh_from_db()
        self.assertEqual(self.event.title, "Updated Event")

    def test_other_user_cannot_edit_event(self):
        client = self.get_auth_client(self.other_user)
        response = client.patch(self.edit_url, {"title": "Hacked Event"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_creator_can_cancel_event(self):
        client = self.get_auth_client(self.creator)
        response = client.post(self.cancel_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.event.refresh_from_db()
        self.assertEqual(self.event.status, "cancelled")

    def test_other_user_cannot_cancel_event(self):
        client = self.get_auth_client(self.other_user)
        response = client.post(self.cancel_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
