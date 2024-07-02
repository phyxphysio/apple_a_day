from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from battery.models import Recipe
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer

RECIPE_URL = reverse("recipe:recipe-list")


def detail_url(recipe_id):
    """Return recipe detail URL."""
    return reverse("recipe:recipe-detail", args=[recipe_id])


def create_recipe(**params):
    """Create and return a new recipe."""
    defaults = {
        "name": "Sample recipe name",
        "description": "Sample recipe description",
        "ingredients": "Sample ingredients",
        "steps": "Sample steps",
    } | params
    return Recipe.objects.create(**defaults)


class PublicRecipeAPITests(TestCase):
    """Test the public recipe API."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_requested(self):
        """Test auth is required for retrieving recipes."""
        res = self.client.get(RECIPE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeAPITests(TestCase):
    """Test the private recipe API."""

    def assert_serializer_equals_response(self, recipes, res):
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user("XXXXXXXXXXXXX", "testpass")
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        """Test retrieving a list of recipes."""
        create_recipe()
        create_recipe(name="Sample recipe name 2")

        res = self.client.get(RECIPE_URL)

        recipes = Recipe.objects.all().order_by("-id")
        self.assert_serializer_equals_response(recipes, res)

    def test_create_recipe(self):
        """Test creating a recipe."""
        payload = {
            "name": "Sample recipe name",
            "description": "Sample recipe description",
            "ingredients": "Sample ingredients",
            "steps": "Sample steps",
        }
        res = self.client.post(RECIPE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data["id"])
        # sourcery skip: no-loop-in-tests
        for key, value in payload.items():
            self.assertEqual(getattr(recipe, key), value)

    def test_recipe_list_limited_to_user(self):
        """Test list of recipes is limited to authenticated user."""
        other_user = get_user_model().objects.create_user("otherUser", "password123")
        create_recipe(user=self.user)
        create_recipe(user=other_user, name="Sample recipe name 2")

        res = self.client.get(RECIPE_URL)

        recipes = Recipe.objects.filter(user=self.user)
        self.assert_serializer_equals_response(recipes, res)
    
    def test_get_recipe_detail(self):
        """Test get recipe detail."""
        recipe = create_recipe(user=self.user)
        url = detail_url(recipe.id)
        res = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.data, serializer.data)
