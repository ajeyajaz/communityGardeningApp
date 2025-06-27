from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from users.models import User
from events.models import Event
from comments.models import Comment
from rest_framework_simplejwt.tokens import RefreshToken

class CommentAPITests(APITestCase):
    def setUp(self):
        # Create users
        self.user = User.objects.create_user(username='ajay', email='ajay@gmail.com', password='testpass123')
        self.other_user = User.objects.create_user(username='guest', email='guest@gmail.com', password='guestpass')

        # Token auth
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        # Create an event
        self.event = Event.objects.create(
            title='Tree Plantation',
            description='Join us for planting!',
            start_date=timezone.now() + timedelta(days=1),
            end_date=timezone.now() + timedelta(days=1, hours=2),
            location_name='Green Garden',
            min_participants=2,
            max_participants=20,
            organizer=self.user
        )

        self.url = f'/api/comments/{self.event.id}/'

    def test_authenticated_user_can_post_comment(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        data = {'content': 'Excited to join!'}
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.first().user, self.user)

    def test_unauthenticated_user_cannot_post_comment(self):
        data = {'content': 'I’m in!'}
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_anyone_can_list_comments(self):
        Comment.objects.create(event=self.event, user=self.user, content="Is there a fee?")
        Comment.objects.create(event=self.event, user=self.other_user, content="Can I bring kids?")

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_no_comments_returns_empty_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])
