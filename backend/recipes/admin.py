from django.contrib.admin import ModelAdmin, register

from .models import (
    Ingredient, IngredientInRecipe, Recipe,
    Tag, ShoppingCart, Follow, Favorite
)


@register(Ingredient)
class IngredientAdmin(ModelAdmin):
    list_display = ('pk', 'title', 'units')
    search_fields = ('name',)


@register(Recipe)
class RecipeAdmin(ModelAdmin):
    list_display = ('pk', 'title', 'author',)
    list_filter = ('author', 'title', 'tags')
    search_fields = ('title',)


@register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ('pk', 'title', 'slug')


@register(IngredientInRecipe)
class IngredientInRecipe(ModelAdmin):
    pass


@register(ShoppingCart)
class ShoppingCartAdmin(ModelAdmin):
    list_display = ('id', 'user', 'recipe')


@register(Follow)
class FollowAdmin(ModelAdmin):
    list_display = ('pk', 'user', 'author')
    search_fields = ('user', 'author')
    list_filter = ('user', 'author')


@register(Favorite)
class FavoriteAdmin(ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
