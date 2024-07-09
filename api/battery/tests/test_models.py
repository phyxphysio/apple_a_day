"""Test models."""

from django.test import TestCase
from django.contrib.auth import get_user_model
from battery import models
import factory

from recipe.tests.test_recipe_api import UserFactory
def create_user():
        defaults = factory.build(dict, FACTORY_CLASS=UserFactory)
        return get_user_model().objects.create(**defaults)

class ModelTests(TestCase):
    
    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = "test@example.com"
        password = "XXXXXXXXXXX"
        user = get_user_model().objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = "test@EXAMPLE.COM"
        user = get_user_model().objects.create_user(email, "test123")

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "test123")

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            "test@example.com",
            "test123",
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
    
    def test_create_recipe(self):
        """ Test creating a recipe."""
        user  = get_user_model().objects.create_user(
            "test@example.com",
            "testpassword123",
        )
        recipe = models.Recipe.objects.create(
            user=user,
            title="Sample recipe name",
            time_minutes=5,
            description="Sample recipe description",
        )
        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        """ Test creating a tag."""
        user = create_user()
        tag = models.Tag.objects.create(
            user=user,
            name="Vegan",
        )
        self.assertEqual(str(tag), tag.name)

    def test_create_ingredient(self):
        """ Test creating an ingredient."""
        user = create_user()
        ingredient = models.Ingredient.objects.create(
            user=user,
            name="Cucumber",
        )
        self.assertEqual(str(ingredient), ingredient.name)