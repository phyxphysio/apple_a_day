from rest_framework import serializers
from battery.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Recipe model allowing all fields to be serialized and setting 'id' as read-only.

    Returns:
        None
    """

    class Meta:
        model = Recipe
        fields = ['id','title','time_minutes','link']
        read_only_fields = ("id",)

class RecipeDetailSerializer(RecipeSerializer):
    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']
