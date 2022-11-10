from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from recipes.models import (
    Ingredient,
    Tag
)
from .serializer import (
    TagSerializer,
    IngredientSerializer,
)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет работы с обьектами класса Tag."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для работы с обьектами класса Ingredient."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    search_fields = ('^name', )
    pagination_class = None
