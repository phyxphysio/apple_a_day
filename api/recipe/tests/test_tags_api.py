from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase
from battery.models import Tag
from recipe.serializers import TagSerializer
from django.urls import reverse
from battery.tests.test_models import create_user

TAG_URL = reverse("recipe:tag-list")

# class PublicTagApiTests(TestCase):
#     """Test the publicly available tags API"""

#     def setUp(self):
#         self.client = APIClient()

#     def test_login_required(self):
#         """Test that login is required for retrieving tags"""
#         res = self.client.get(TAG_URL)

#         self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)