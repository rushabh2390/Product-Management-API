from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from rest_framework import status
from .models import Category

class CategoryViewSetTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'password')
        self.regular_user = User.objects.create_user('user', 'user@example.com', 'password')
        self.category = Category.objects.create(category_name='Electronics', description='Devices including smartphones, laptops, and accessories')

    def test_list_categories_as_regular_user(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get('/category/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_category_as_regular_user(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(f'/category/{self.category.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_category_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {'category_name': 'Books', 'description': 'All kinds of books'}
        response = self.client.post('/category/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_category_as_regular_user(self):
        self.client.force_authenticate(user=self.regular_user)
        data = {'category_name': 'Books', 'description': 'All kinds of books'}
        response = self.client.post('/category/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_category_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {'category_name': 'Updated Electronics', 'description': 'Updated description'}
        response = self.client.put(f'/category/{self.category.pk}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_category_as_regular_user(self):
        self.client.force_authenticate(user=self.regular_user)
        data = {'category_name': 'Updated Electronics', 'description': 'Updated description'}
        response = self.client.put(f'/category/{self.category.pk}/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_category_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(f'/category/{self.category.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_category_as_regular_user(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.delete(f'/category/{self.category.pk}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
