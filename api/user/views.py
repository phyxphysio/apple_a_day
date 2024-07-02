from user.serializers import UserSerializer, AuthTokenSerializer
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings


class CreateUserView(generics.CreateAPIView):
    """
    View for creating a new user instance using the UserSerializer.

    Returns:
        None
    """

    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """
    View for creating an authentication token using the AuthTokenSerializer.

    Returns:
        None
    """

    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class ManageUserView(generics.RetrieveUpdateAPIView):
    """
    View for managing the authenticated user using the UserSerializer.

    Returns:
        None
    """

    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """
        Retrieves the authenticated user object.

        Returns:
            User: The authenticated user object.
        """

        return self.request.user