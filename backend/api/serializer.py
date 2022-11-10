import base64

from django.core.files.base import ContentFile
from djoser.serializers import UserSerializer
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from recipes.models import Tag, Ingredient, Recipe, IngredientInRecipe


class Base64ImageField(serializers.ImageField):
    """Кастомное поле для кодирования изображения в base64."""
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='photo.' + ext)

        return super().to_internal_value(data)


class TagSerializer(ModelSerializer):
    """Сериализатор для вывода тэгов."""
    class Meta:
        model = Tag
        fields = ('id', 'title', 'hexcolor', 'slug')
        read_only_fields = ('id', 'title', 'hexcolor', 'slug',)


class IngredientSerializer(ModelSerializer):
    """Сериализатор для вывода ингридиентов."""
    class Meta:
        model = Ingredient
        fields = ('id', 'title', 'units',)
        read_only_fields = ('id', 'title', 'units',)


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели ингридиентов в рецепте."""

    id = serializers.ReadOnlyField(
        source='ingredient.id'
    )
    title = serializers.ReadOnlyField(
        source='ingredient.title'
    )
    units = serializers.ReadOnlyField(
        source='ingredient.units'
    )

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'title', 'units', 'amount')


class RecipeSerializer(ModelSerializer):
    """Сериализатор для рецептов."""
    tags = TagSerializer(
        many=True,
        read_only=True
    )
    author = UserSerializer(
        read_only=True
    )
    ingredients = IngredientInRecipeSerializer(
        source='ingredient_amounts',
        many=True,
        read_only=True
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'author',
            'title',
            'image',
            'description',
            'ingredients',
            'tags',
            'cooking_time',
        )


class AddIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор модели ингридиентов в рецепте для добавления."""
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'amount')
