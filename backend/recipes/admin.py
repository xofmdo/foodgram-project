from django.contrib.admin import ModelAdmin, register

from .models import Ingredient, IngredientInRecipe, Recipe, Tag


@register(Ingredient)
class IngredientAdmin(ModelAdmin):
    list_display = (
        'title', 'units',
    )
    search_fields = (
        'title',
    )
    list_filter = (
        'title',
    )


@register(Recipe)
class RecipeAdmin(ModelAdmin):
    list_display = (
        'title', 'author',
    )
    fields = (
        ('title', 'cooking_time',),
        ('author', 'tags',),
        ('description',),
        ('image',),
    )
    raw_id_fields = ('author', )
    search_fields = (
        'title', 'author',
    )
    list_filter = (
        'title', 'author__username',
    )


@register(Tag)
class TagAdmin(ModelAdmin):
    list_display = (
        'title', 'color', 'slug',
    )
    search_fields = (
        'title', 'color'
    )


@register(IngredientInRecipe)
class IngredientInRecipe(ModelAdmin):
    pass
