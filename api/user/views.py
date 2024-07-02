from user.serializers import UserSerializer
from rest_framework import generics


class CreateUserView(generics.CreateAPIView):
    """
    View for creating a new user instance using the UserSerializer.

    Returns:
        None
    """

    serializer_class = UserSerializer
