from rest_framework.test import APITestCase, APIClient
from users.models import User
from django.utils import timezone
from datetime import timedelta
from events.models import Event,EventParticipant
from rest_framework_simplejwt.tokens import RefreshToken

class EventListCreateAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='ajay123',
            email='ajay89@gmail.com',
            password='testpass123'
        )
        self.client = APIClient()

        # Set JWT access token for authenticated requests
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)

        self.url = '/api/events/'

    """
                 Event creation test cases
    """
    def test_unauthenticated_user_can_list_events(self):
        Event.objects.create(
            title='Test Event',
            description='Gardening fun',
            start_date=timezone.now() + timedelta(days=2),
            end_date=timezone.now() + timedelta(days=2, hours=2),
            location_name='Green Park',
            min_participants=3,
            max_participants=20,
            organizer=self.user
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_authenticated_user_can_create_event(self):
        data = {
            "title": "Garden Meetup",
            "description": "Bring your tools!",
            "start_date": (timezone.now() + timedelta(days=3)).isoformat(),
            "end_date": (timezone.now() + timedelta(days=3, hours=2)).isoformat(),
            "location_name": "Botanical Garden",
            "min_participants": 2,
            "max_participants": 15,
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Event.objects.count(), 1)
        self.assertEqual(Event.objects.first().organizer, self.user)

    def test_unauthenticated_user_cannot_create_event(self):
        # Clear token to simulate unauthenticated user
        self.client.credentials()

        data = {
            "title": "Unauthorized Event",
            "description": "No login",
            "start_date": (timezone.now() + timedelta(days=1)).isoformat(),
            "end_date": (timezone.now() + timedelta(days=1, hours=1)).isoformat(),
            "location_name": "Unknown",
            "min_participants": 1,
            "max_participants": 5,
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 401)

    def test_max_participants_less_than_min_participants(self):
        data = {
            "title": "Broken Event",
            "description": "Invalid numbers",
            "start_date": (timezone.now() + timedelta(days=2)).isoformat(),
            "end_date": (timezone.now() + timedelta(days=2, hours=2)).isoformat(),
            "location_name": "Bad Garden",
            "min_participants": 10,
            "max_participants": 5,  # invalid
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_end_date_before_start_date(self):
        start = timezone.now() + timedelta(days=3)
        end = timezone.now() + timedelta(days=2)  # earlier than start
        data = {
            "title": "Time Travel Event",
            "description": "Backwards",
            "start_date": start.isoformat(),
            "end_date": end.isoformat(),
            "location_name": "Reverse Garden",
            "min_participants": 2,
            "max_participants": 10,
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_start_date_in_past(self):
        data = {
            "title": "Old Event",
            "description": "Too late",
            "start_date": (timezone.now() - timedelta(days=1)).isoformat(),  # in the past
            "end_date": timezone.now().isoformat(),
            "location_name": "History Garden",
            "min_participants": 2,
            "max_participants": 10,
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_missing_required_field_title(self):
        data = {
            # "title" is missing
            "description": "Missing title",
            "start_date": (timezone.now() + timedelta(days=2)).isoformat(),
            "end_date": (timezone.now() + timedelta(days=2, hours=2)).isoformat(),
            "location_name": "Title-less Garden",
            "min_participants": 1,
            "max_participants": 5,
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)


        """
                Event search test cases
        """

    def test_filter_events_by_location(self):
        Event.objects.create(
            title='Park Event',
            description='Green fun',
            start_date=timezone.now() + timedelta(days=2),
            end_date=timezone.now() + timedelta(days=2, hours=2),
            location_name='Central Park',
            min_participants=2,
            max_participants=20,
            organizer=self.user
        )
        Event.objects.create(
            title='Beach Event',
            description='Sandy vibes',
            start_date=timezone.now() + timedelta(days=2),
            end_date=timezone.now() + timedelta(days=2, hours=2),
            location_name='Sunny Beach',
            min_participants=2,
            max_participants=20,
            organizer=self.user
        )

        response = self.client.get(self.url + '?location_name=Central Park')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['location_name'], 'Central Park')

    def test_filter_events_by_start_date(self):
        today = timezone.now().date()

        Event.objects.create(
            title='Today Event',
            description='Today gardening',
            start_date=timezone.now().replace(hour=10, minute=0),
            end_date=timezone.now().replace(hour=12, minute=0),
            location_name='City Garden',
            min_participants=3,
            max_participants=30,
            organizer=self.user
        )

        Event.objects.create(
            title='Tomorrow Event',
            description='Another day',
            start_date=timezone.now() + timedelta(days=1),
            end_date=timezone.now() + timedelta(days=1, hours=1),
            location_name='Botanical',
            min_participants=3,
            max_participants=30,
            organizer=self.user
        )

        date_str = today.isoformat()
        response = self.client.get(self.url + f'?start_date={date_str}')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(any(date_str in event['start_date'] for event in response.data))

    def test_filter_events_by_organizer(self):
        other_user = User.objects.create_user(username='otherguy', password='otherpass')

        Event.objects.create(
            title='Ajay Event',
            description='Ajay only',
            start_date=timezone.now() + timedelta(days=2),
            end_date=timezone.now() + timedelta(days=2, hours=2),
            location_name='Home Garden',
            min_participants=3,
            max_participants=10,
            organizer=self.user
        )

        Event.objects.create(
            title='Other User Event',
            description='Not Ajay',
            start_date=timezone.now() + timedelta(days=3),
            end_date=timezone.now() + timedelta(days=3, hours=2),
            location_name='Far Garden',
            min_participants=3,
            max_participants=10,
            organizer=other_user
        )

        response = self.client.get(self.url + f'?organizer={self.user.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['organizer'], self.user.id)

