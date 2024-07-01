from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **other_fields):
        """
        Manages the creation of user instances.

        Args:
            email: The email address of the user.
            password: The password for the user.
            name: The name of the user.
            other_fields: Additional fields for the user.

        Returns:
            User: The created user instance.

        Raises:
            ValueError: If the email is not provided.

        Examples:
            Creating a user with the specified email and optional password or name.
        """

        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(email=self.normalize_email(email), **other_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name):
        """
        Creates a superuser with elevated permissions.

        Args:
            email: The email address of the superuser.
            name: The name of the superuser.

        Returns:
            User: The created superuser instance.
        """

        user = self.create_user(
            email,
            name,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model with email as the unique identifier.

    Returns:
        str: The email address of the user.
    """

    email = models.EmailField(unique=True, max_length=255)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]
    objects = UserManager()

    def __str__(self):
        return self.email


class Energy(models.Model):
    """
    Model to store energy-related data including wellbeing, mental stress, physical stress, and date added.

    Returns:
        None
    """

    wellbeing = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Enter a value from 1 (very unwell) to 10 (extremely well)",
    )
    mental_stress = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Enter a value from 1 (no stress) to 10 (extremely stressed)",
    )
    physical_stress = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Enter a value from 1 (no stress) to 10 (extremely stressed)",
    )
    date_added = models.DateTimeField(auto_now_add=True)
