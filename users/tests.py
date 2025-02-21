from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from .models import CustomerUser  # Replace .models with your app's models
# Replace .serializers with your app's serializers
from .serializers import RegistrationSerializer, LoginSerializer, UserUpdateSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.core import mail
from django.conf import settings
from unittest.mock import patch
from django.test.utils import override_settings
import json


class TestsAuth(TestCase):
    def setUp(self):
        self.client = Client()
        # Replace 'register' with your URL name
        self.registration_url = reverse('register')
        self.login_url = reverse('login')  # Replace 'login' with your URL name
        # Replace 'logout' with your URL name
        self.logout_url = reverse('logout')
        # Replace 'user-update' with your URL name
        self.user_update_url = reverse('user-update')
        # Replace 'forgot-password' with your URL name
        self.forgot_password_url = reverse('forgot-password')

        self.user_data = {
            'email': 'test@example.com',
            'password': 'testpassword',
            'username': 'test',
            # Add other required fields for registration
            'first_name': 'Test',
            'last_name': 'User',
            'is_staff': False,
            'is_active': True
        }
        self.invalid_user_data = {
            'email': 'invalid-email',  # Invalid email
            'password': 'testpassword',
            # Add other required fields for registration
            'first_name': 'Test',
            'last_name': 'User',
            'username': 'test',
            'is_staff': False,
            'is_active': True
        }
        self.login_data = {
            'email': 'test@example.com',
            'password': 'testpassword'
        }

    def test_registration(self):
        response = self.client.post(
            self.registration_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomerUser.objects.count(), 1)
        self.assertEqual(CustomerUser.objects.get(
            email=self.user_data['email']).email, self.user_data['email'])

    def test_registration_invalid_data(self):
        response = self.client.post(
            self.registration_url, self.invalid_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(CustomerUser.objects.count(), 0)

    def test_login(self):
        # First register a user
        self.client.post(self.registration_url, self.user_data, format='json')
        response = self.client.post(
            self.login_url, self.login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)

    def test_login_invalid_credentials(self):
        response = self.client.post(self.login_url, {
                                    'email': 'wrong@example.com', 'password': 'wrongpassword'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)

    def test_logout(self):
        # Register and login a user to get a refresh token
        self.client.post(self.registration_url, self.user_data, format='json')
        login_response = self.client.post(
            self.login_url, self.login_data, format='json')
        refresh_token = login_response.data['refresh']

        response = self.client.post(
            self.logout_url, {'refresh': refresh_token}, format='json')
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

        # Try using the blacklisted refresh token, should fail
        # You'll need to add logic to your test to check if the token is actually blacklisted.
        # This part depends on how you handle blacklisting in your application.  It might involve
        # trying to get a new access token with the refresh token and checking if it fails.

    def test_user_update(self):
        # Register and login a user
        self.client.post(self.registration_url, self.user_data, format='json')
        login_response = self.client.post(
            self.login_url, self.login_data, format='json')
        access_token = login_response.data['access']
        updated_data = json.dumps({"first_name": "Updated"})
        response = self.client.patch(self.user_update_url, updated_data,content_type='application/json', headers={"Authorization": f'Bearer {access_token}'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Updated')

    def test_forgot_password(self):
        # Register a user
        self.client.post(self.registration_url, self.user_data, format='json')
        response = self.client.post(self.forgot_password_url, json.dumps({
                                    'email': self.user_data['email']}), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_forgot_password_user_not_found(self):
        response = self.client.post(self.forgot_password_url, {
                                    'email': 'nonexistent@example.com'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Add more test cases for edge cases and error handling as needed.
    # For example, test with missing required fields in the serializers, invalid data types, etc.
