from rest_framework import serializers
from battery.models import Recipe, Tag, Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ["id", "name"]
        read_only_fields = ("id",)


class TagSerializer(serializers.ModelSerializer):
    """
    Serializer class for serializing Tag instances.

    Explanation:
    This serializer class defines how Tag instances should be serialized, specifying the model, fields to include, and read-only fields.

    Attributes:
        model: The model to be serialized.
        fields (list): The fields to be serialized.
        read_only_fields (tuple): The fields that are read-only during serialization.
    """

    class Meta:
        model = Tag
        fields = ["id", "name"]
        read_only_fields = ("id",)


class RecipeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Recipe model allowing all fields to be serialized and setting 'id' as read-only.

    Returns:
        None
    """

    tags = TagSerializer(many=True, required=False)
    ingredients = IngredientSerializer(many=True, required=False)

    class Meta:
        """
        Meta class configuration for the RecipeSerializer.

        Explanation:
        This Meta class defines the configuration options for the RecipeSerializer, including the model to serialize, fields to include, and read-only fields.

        Attributes:
            model: The model to be serialized.
            fields (list): The fields to be serialized.
            read_only_fields (tuple): The fields that are read-only during serialization.
        """

        model = Recipe
        fields = ["id", "title", "time_minutes", "link", "tags", "ingredients"]
        read_only_fields = ("id",)

    def create(self, validated_data):
        """Create a recipe."""
        tags = validated_data.pop("tags", [])
        ingredients = validated_data.pop("ingredients", [])
        recipe = Recipe.objects.create(**validated_data)
        self._get_or_create_tags(tags, recipe)
        self._get_or_create_ingredients(ingredients, recipe)

        return recipe

    def update(self, instance, validated_data):
        """Update recipe."""
        tags = validated_data.pop("tags", None)
        ingredients = validated_data.pop("ingredients", None)
        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)
        if ingredients is not None:
            instance.ingredients.clear()
            self._get_or_create_ingredients(ingredients, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

    def _get_or_create_ingredients(self, ingredients, recipe):
        for ingredient_data in ingredients:
            ingredient, _ = Ingredient.objects.get_or_create(user=self.context['request'].user,**ingredient_data)
            recipe.ingredients.add(ingredient)

    def _get_or_create_tags(self, tags, recipe):
        for tag_data in tags:
            tag, _ = Tag.objects.get_or_create(user=self.context['request'].user, **tag_data)
            recipe.tags.add(tag)


class RecipeDetailSerializer(RecipeSerializer):
    """
    A serializer class for detailed representation of a recipe, extending the base RecipeSerializer.

    Explanation:
    This serializer includes the base fields from RecipeSerializer along with the 'description' field for a more detailed representation of a recipe.

    Attributes:
        fields (list): The fields to be serialized, including those from RecipeSerializer and 'description'.
    """

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ["description"]
