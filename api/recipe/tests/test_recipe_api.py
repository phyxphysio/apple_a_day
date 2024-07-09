from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient
from battery.models import Recipe, Tag, Ingredient
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
        if "user" not in defaults:
            defaults["user"] = self.user
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

    def test_full_update(self):
        """Test full update of a recipe."""
        recipe = self.create_recipe()

        payload = factory.build(dict, FACTORY_CLASS=RecipeFactory)
        url = detail_url(recipe.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(recipe, k), v)
        self.assertEqual(recipe.user, self.user)

    def test_update_user_returns_error(self):
        """Test changing the recipe user results in an error."""
        new_user = self.create_user()
        recipe = self.create_recipe()

        payload = {"user": new_user.id}
        url = detail_url(recipe.id)
        self.client.patch(url, payload)

        recipe.refresh_from_db()
        self.assertEqual(recipe.user, self.user)

    def test_delete_recipe(self):
        """Test deleting a recipe successful."""
        recipe = self.create_recipe()

        url = detail_url(recipe.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Recipe.objects.filter(id=recipe.id).exists())

    def test_delete_other_users_recipe_error(self):
        """Test trying to delete another user's recipe results in an error."""
        new_user = self.create_user()
        recipe = self.create_recipe(user=new_user)

        url = detail_url(recipe.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Recipe.objects.filter(id=recipe.id).exists())

    def test_create_recipe_with_new_tags(self):
        """Test creating a recipe with new tags."""
        payload = factory.build(
            dict,
            FACTORY_CLASS=RecipeFactory,
            tags=[{"name": "new tag"}],
        )
        res = self.client.post(RECIPE_URL, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data["id"])
        self.assertEqual(recipe.tags.count(), 1)
        self.assertEqual(recipe.tags.first().name, "new tag")

    def test_create_recipe_with_existing_tags(self):
        """Test creating a recipe with existing tag."""
        tag = Tag.objects.create(user=self.user, name="Existing Tag")
        payload = factory.build(
            dict, FACTORY_CLASS=RecipeFactory, tags=[{"name": "Existing Tag"}]
        )
        res = self.client.post(RECIPE_URL, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data["id"])
        self.assertEqual(recipe.tags.count(), 1)
        self.assertEqual(recipe.tags.first(), tag)

    def test_create_tag_on_update(self):
        """Test creating tag when updating a recipe."""
        recipe = self.create_recipe()
        payload = {"tags": [{"name": "new tag"}]}
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(recipe.tags.count(), 1)
        self.assertEqual(recipe.tags.first().name, "new tag")

    def test_update_recipe_assign_tag(self):
        """Test assigning an existing tag when updating a recipe."""
        tag1 = Tag.objects.create(user=self.user, name="Tag 1")
        recipe = self.create_recipe()
        recipe.tags.add(tag1)
        tag2 = Tag.objects.create(user=self.user, name="Tag 2")
        payload = {"tags": [{"name": "Tag 2"}]}
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(recipe.tags.count(), 1)
        self.assertEqual(recipe.tags.first(), tag2)

    def test_clear_recipe_tags(self):
        """Test clearing all tags from a recipe."""
        tag = Tag.objects.create(user=self.user, name="Tag")
        recipe = self.create_recipe()
        recipe.tags.add(tag)
        payload = {"tags": []}
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(recipe.tags.count(), 0)

    def test_create_recipe_with_no_tags(self):
        """Test creating a recipe with no tags."""
        payload = factory.build(dict, FACTORY_CLASS=RecipeFactory, tags=[])
        res = self.client.post(RECIPE_URL, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data["id"])
        self.assertEqual(recipe.tags.count(), 0)

    def test_create_recipe_with_new_ingredients(self):
        """Test creating a recipe with new ingredients."""
        payload = factory.build(
            dict,
            FACTORY_CLASS=RecipeFactory,
            ingredients=[{"name": "new ingredient"}],
        )
        res = self.client.post(RECIPE_URL, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data["id"])
        self.assertEqual(recipe.ingredients.count(), 1)
        self.assertEqual(recipe.ingredients.first().name, "new ingredient")

    def test_create_recipe_with_existing_ingredients(self):
        """Test creating a recipe with existing ingredient."""
        ingredient = Ingredient.objects.create(
            user=self.user, name="Existing Ingredient"
        )
        payload = factory.build(
            dict,
            FACTORY_CLASS=RecipeFactory,
            ingredients=[{"name": "Existing Ingredient"}],
        )
        res = self.client.post(RECIPE_URL, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data["id"])
        self.assertEqual(recipe.ingredients.count(), 1)
        self.assertEqual(recipe.ingredients.first(), ingredient)

    def test_create_ingredient_on_update(self):
        """Test creating ingredient when updating a recipe."""
        recipe = self.create_recipe()
        payload = {"ingredients": [{"name": "new ingredient"}]}
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(recipe.ingredients.count(), 1)
        self.assertEqual(recipe.ingredients.first().name, "new ingredient")

    def test_assign_ingredient_to_recipe(self):
        """Test assigning an existing ingredient to a recipe."""
        ingredient1 = Ingredient.objects.create(user=self.user, name="Ingredient 1")
        recipe = self.create_recipe()
        recipe.ingredients.add(ingredient1)
        ingredient2 = Ingredient.objects.create(user=self.user, name="Ingredient 2")
        payload = {"ingredients": [{"name": "Ingredient 2"}]}
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(recipe.ingredients.count(), 1)
        self.assertEqual(recipe.ingredients.first(), ingredient2)

    def test_clear_recipe_ingredients(self):
        """Test clearing all ingredients from a recipe."""
        ingredient = Ingredient.objects.create(user=self.user, name="Ingredient")
        recipe = self.create_recipe()
        recipe.ingredients.add(ingredient)
        payload = {"ingredients": []}
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(recipe.ingredients.count(), 0)

