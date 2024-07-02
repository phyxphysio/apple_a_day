"""Tests for usr api."""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse("user:create")


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class publicUserApiTests(TestCase):
    """Test the publicly available user API"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
            "email": "test@example.com",
            "password": "XXXXXXXX",
            "name": "Test Name",
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        usr = get_user_model().objects.get(email=payload["email"])
        self.assertTrue(usr.check_password(payload["password"]))
        self.assertNotIn("password", res.data)

    def test_user_exists(self):
        """Test creating a user that already exists fails"""
        payload = {
            "email": "test@example.com",
            "password": "XXXXXXXX",
            "name": "Test Name",
        }
        create_user(
            email="test@example.com",
            password="XXXXXXXX",
            name="Test Name",
        )
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the password must be more than 5 characters."""
        payload = {
            "email": "test@example.com",
            "password": "1234",
            "name": "Test Name",
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=payload["email"]).exists()

        self.assertFalse(user_exists)