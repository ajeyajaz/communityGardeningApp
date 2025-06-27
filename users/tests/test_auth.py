from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User

class AuthAPITests(APITestCase):
    def setUp(self):
        self.register_url = '/api/user/signup/'
        self.login_url = '/api/user/login/'

    def test_user_can_register_with_email(self):
        data = {
            "username": "ajay",
            "email": "ajay@example.com",
            "password": "strongpass123"
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="ajay@example.com").exists())

    def test_registration_fails_without_email(self):
        data = {
            "username": "ajay",
            "password": "strongpass123"
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_login_with_correct_credentials(self):
        User.objects.create_user(username="ajay", email="ajay@gmail.com", password="testpass123")
        data = {
            "username": "ajay",
            "password": "testpass123"
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_fails_with_wrong_password(self):
        User.objects.create_user(username="ajay", email="ajay@gmail.com", password="testpass123")
        data = {
            "username": "ajay",
            "password": "wrongpass"
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
