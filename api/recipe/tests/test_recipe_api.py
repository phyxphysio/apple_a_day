from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from battery.models import Recipe
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer
import factory

RECIPE_URL = reverse("recipe:recipe-list")


class RecipeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Recipe
    title = factory.Sequence(lambda n: f"Recipe {n}")
    description = factory.Faker("sentence")
    time_minutes = factory.Faker("random_int", min=1, max=120)
    link = factory.Faker("uri")


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    email = factory.Faker("email")
    password = factory.Faker("password")


def detail_url(recipe_id):
    """Return recipe detail URL."""
    return reverse("recipe:recipe-detail", args=[recipe_id])

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
        self.user = self.create_user()
        self.client.force_authenticate(self.user)

    def create_recipe(self, **params):
        """Create and return a new recipe."""
        defaults = factory.build(dict, FACTORY_CLASS=RecipeFactory) | params
        if 'user' not in defaults:
            defaults['user'] = self.user
        return Recipe.objects.create(**defaults)


    def create_user(self, **params):
        """Create and return a new user."""
        defaults = factory.build(dict, FACTORY_CLASS=UserFactory) | params
        return get_user_model().objects.create_user(**defaults)

    def test_retrieve_recipes(self):
        """Test retrieving a list of recipes."""
        self.create_recipe()
        self.create_recipe()

        res = self.client.get(RECIPE_URL)

        recipes = Recipe.objects.all().order_by("-id")
        self.assert_serializer_equals_response(recipes, res)

    def test_create_recipe(self):
        """Test creating a recipe."""
        payload = factory.build(dict, FACTORY_CLASS=RecipeFactory)
        res = self.client.post(RECIPE_URL, payload)
        print(res.data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data["id"])
        # sourcery skip: no-loop-in-tests
        for key, value in payload.items():
            self.assertEqual(getattr(recipe, key), value)
        self.assertEqual(recipe.user, self.user)

    def test_recipe_list_limited_to_user(self):
        """Test list of recipes is limited to authenticated user."""
        other_user = self.create_user()
        self.create_recipe()
        self.create_recipe(user=other_user)

        res = self.client.get(RECIPE_URL)
        recipes = Recipe.objects.filter(user=self.user)
        self.assert_serializer_equals_response(recipes, res)

    def test_get_recipe_detail(self):
        """Test get recipe detail."""
        recipe = self.create_recipe()
        url = detail_url(recipe.id)
        res = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.data, serializer.data)

    def test_partial_update(self):
        """Test partial update of a recipe."""
        original_link = "https://www.example.com"
        recipe = self.create_recipe()

        payload = factory.build(
            dict,
            FACTORY_CLASS=RecipeFactory,
            link=original_link,
        )
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        self.assertEqual(recipe.title, payload["title"])
        self.assertEqual(recipe.link, original_link)
        self.assertEqual(recipe.user, self.user)
        self.assertEqual(1,2)