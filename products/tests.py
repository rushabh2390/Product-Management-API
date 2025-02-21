from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from .models import Product  # Replace .models with your actual app.models
# Replace .serializers with your actual app.serializers
from .serializers import ProductSerializer
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from categories.models import Category
import json


class ProductViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            'admin', 'admin@example.com', 'password')
        self.regular_user = User.objects.create_user(
            'user', 'user@example.com', 'password')
        self.category = Category.objects.create(
            category_name='Electronics', description='Devices including smartphones, laptops, and accessories')
        self.product_data = {
            'product_name': 'Test Product',
            'product_description': 'Test Description',
            'product_price': 10.99,
            "currency": "INR",
            "stock_quantity": 100,
            "sku": "TEST-001",
            "image_url": "https://example.com/test.jpg",
            "category": self.category
        }

        # Create a product for detail, update, delete tests
        self.product = Product.objects.create(**self.product_data)

    def test_list_products_as_regular_user(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get('/product/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_product_as_regular_user(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(f'/product/{self.product.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_product_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'product_name': 'Test Product2',
            'product_description': 'Test2',
            'product_price': 20.99,
            "currency": "INR",
            "stock_quantity": 200,
            "sku": "TEST-002",
            "image_url": "https://example.com/test2.jpg",
            "category": self.category.pk
        }
        response = self.client.post('/product/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_product_as_regular_user(self):
        self.client.force_authenticate(user=self.regular_user)
        data = {
            'product_name': 'Test Product3',
            'product_description': 'Test3',
            'product_price': 30.99,
            "currency": "INR",
            "stock_quantity": 300,
            "sku": "TEST-003",
            "image_url": "https://example.com/test3.jpg",
            "category": self.category.pk
        }
        response = self.client.post('/product/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_product_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'product_name': 'Updated',
            'product_description': 'Update Description'
        }
        response = self.client.patch(f'/product/{self.product.pk}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_product_as_regular_user(self):
        self.client.force_authenticate(user=self.regular_user)
        data = {
            'product_name': 'Update',
            'product_description': 'Regular User update it'
        }
        response = self.client.put(f'/product/{self.product.pk}/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_product_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(f'/product/{self.product.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_product_as_regular_user(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.delete(f'/product/{self.product.pk}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
