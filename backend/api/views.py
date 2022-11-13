from _csv import writer

from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from djoser.serializers import TokenCreateSerializer, TokenSerializer
from djoser.views import UserViewSet, TokenCreateView
from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (
    AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
)
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from rest_framework.viewsets import ModelViewSet
from djoser import utils
from recipes.models import (
    Ingredient, Tag, Recipe, Favorite, ShoppingCart, Follow,
    IngredientInRecipe,
)
from users.models import User
from .pagination import CustomPagination
from .permissions import IsAuthorOrReadOnly
from .serializer import (
    TagSerializer,
    IngredientSerializer,
    RecipeSerializer, CustomUserSerializer, CreateRecipeSerializer,
    FollowSerializer, AddFavoritesSerializer,
)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет работы с обьектами класса Tag."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для работы с обьектами класса Ingredient."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)


class CustomUserViewSet(UserViewSet):
    """Вьюсет для работы с обьектами класса User и подписки на авторов."""

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (AllowAny,)
    # permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = LimitOffsetPagination

    @action(
        detail=False,
        methods=('get',),
        permission_classes=(IsAuthenticated, ),
        url_path='subscriptions',
        url_name='subscriptions',
    )
    def subscriptions(self, request):
        queryset = User.objects.filter(follow__user=self.request.user)
        if queryset:
            pages = self.paginate_queryset(queryset)
            serializer = FollowSerializer(pages, many=True,
                                          context={'request': request})
            return self.get_paginated_response(serializer.data)
        return Response('Вы ни на кого не подписаны.',
                        status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(IsAuthenticated,),
        url_path='subscribe',
        url_name='subscribe',
    )
    def subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(User, id=id)
        change_subscription_status = Follow.objects.filter(
            user=user.id, author=author.id
        )
        if request.method == 'POST':
            if user == author:
                return Response('Вы пытаетесь подписаться на себя!!',
                                status=status.HTTP_400_BAD_REQUEST)
            if change_subscription_status.exists():
                return Response(f'Вы теперь подписаны на {author}',
                                status=status.HTTP_400_BAD_REQUEST)
            subscribe = Follow.objects.create(
                user=user,
                author=author
            )
            subscribe.save()
            return Response(f'Вы подписались на {author}',
                            status=status.HTTP_201_CREATED)
        if change_subscription_status.exists():
            change_subscription_status.delete()
            return Response(f'Вы отписались от {author}',
                            status=status.HTTP_204_NO_CONTENT)
        return Response(f'Вы не подписаны на {author}',
                        status=status.HTTP_400_BAD_REQUEST)


class RecipeViewSet(ModelViewSet):
    """ViewSet для обработки запросов, связанных с рецептами."""
    queryset = Recipe.objects.all()
    lookup_field = 'id'
    pagination_class = CustomPagination
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeSerializer
        elif self.action in ('create', 'partial_update'):
            return CreateRecipeSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(IsAuthenticated,),
        url_path='favorite',
        url_name='favorite',
    )
    def favorite(self, request, pk):
        if request.method == 'POST':
            user = request.user
            recipe = get_object_or_404(Recipe, id=pk)
            if Favorite.objects.filter(user=user, recipe=recipe).exists():
                return Response(
                    {'errors': f'Повторно - \"{recipe.name}\" добавить нельзя,'
                               f'он уже есть в избранном у пользователя'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            Favorite.objects.create(user=user, recipe=recipe)
            serializer = AddFavoritesSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            user = request.user
            recipe = get_object_or_404(Recipe, id=pk)
            obj = Favorite.objects.filter(user=user, recipe__id=pk)
            if obj.exists():
                obj.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {'errors': f'В избранном нет рецепта \"{recipe.name}\"'},
                status=HTTP_400_BAD_REQUEST
            )

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(IsAuthenticated,),
        url_path='shopping_cart',
        url_name='shopping_cart',
    )
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            user = request.user
            recipe = get_object_or_404(Recipe, id=pk)
            if ShoppingCart.objects.filter(user=user, recipe=recipe).exists():
                return Response(
                    {'errors': f'Повторно - \"{recipe.name}\" добавить нельзя,'
                               f'он уже есть в списке покупок'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            ShoppingCart.objects.create(user=user, recipe=recipe)
            serializer = AddFavoritesSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            user = request.user
            recipe = get_object_or_404(Recipe, id=pk)
            obj = ShoppingCart.objects.filter(user=user, recipe__id=pk)
            if obj.exists():
                obj.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {'errors': f'Нельзя удалить рецепт - \"{recipe.name}\", '
                           f'которого нет в списке покупок '},
                status=HTTP_400_BAD_REQUEST
            )

    @staticmethod
    def ingredients_to_txt(ingredients):
        shopping_list = ''
        for ingredient in ingredients:
            shopping_list += (
                f"{ingredient['ingredient__name']} "
                f"({ingredient['ingredient__measurement_unit']}) - "
                f"{ingredient['sum']}\n"
            )
        return shopping_list

    @action(
        detail=False,
        methods=('get',),
        permission_classes=(IsAuthenticated,),
        url_path='download_shopping_cart',
        url_name='download_shopping_cart',
    )
    def download_shopping_cart(self, request):
        ingredients = IngredientInRecipe.objects.filter(
            recipe__shopping_recipe__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(sum=Sum('amount'))
        shopping_list = self.ingredients_to_txt(ingredients)
        return HttpResponse(shopping_list, content_type='text/plain')
