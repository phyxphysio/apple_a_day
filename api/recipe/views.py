from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from battery.models import Recipe, Tag, Ingredient
from recipe.serializers import (
    RecipeSerializer,
    RecipeDetailSerializer,
    TagSerializer,
    IngredientSerializer,
)


class RecipeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the Recipe model allowing full CRUD operations via the API.

    Attributes:
        queryset (QuerySet): The queryset of Recipe objects to be used by the ViewSet.
        serializer_class (Serializer): The serializer class to be used for converting Recipe objects to and from JSON.
        authentication_classes (tuple): The authentication classes to be used by the ViewSet.
        permission_classes (tuple): The permission classes to be used by the ViewSet.

    Methods:
        list: Retrieves a list of Recipe objects.
        create: Creates a new Recipe object.
        retrieve: Retrieves a specific Recipe object.
        update: Updates a specific Recipe object.
        partial_update: Partially updates a specific Recipe object.
        destroy: Deletes a specific Recipe object.
    """

    queryset = Recipe.objects.all()
    serializer_class = RecipeDetailSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        Retrieves the queryset of Recipe objects for the current user.

        Returns:
            QuerySet: The queryset of Recipe objects for the current user.
        """
        return Recipe.objects.filter(user=self.request.user).order_by("-id")

    def get_serializer_class(self):
        if self.action == "list":
            return RecipeSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BaseRecipeAttrViewSet(
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """
    Base ViewSet for retrieving a list of recipe attributes (tags and ingredients).

    Attributes:
        queryset (QuerySet): The queryset of recipe attributes to be used by the ViewSet.

    Methods:
        list: Retrieves a list of recipe attributes.
    """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class IngredientViewSet(BaseRecipeAttrViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()


class TagViewSet(BaseRecipeAttrViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
