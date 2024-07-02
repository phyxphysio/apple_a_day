from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializers for user model."""

    class Meta:
        model = get_user_model()
        fields = ("email", "password", "name")
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        """
        Creates a user instance based on the validated data.

        Args:
            validated_data: The validated data for creating the user.

        Returns:
            User: The created user instance.
        """

        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """
        Updates a user instance with the validated data.

        Args:
            instance: The user instance to be updated.
            validated_data: The validated data for updating the user.

        Returns:
            User: The updated user instance.
        """

        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for authentication token."""

    email = serializers.EmailField(label=_("Email"))
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        write_only=True,
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(
                request=self.context.get("request"), username=email, password=password
            )
            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = _("Both Email and password are required.")
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs
