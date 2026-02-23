from django.contrib import admin

from .models import FoodQuality, Recipe, FoodItemSource, FoodItemDLC, RecipeIngredient


@admin.register(FoodQuality)
class FoodQualityAdmin(admin.ModelAdmin):
    list_display = ('id', 'quality', 'morale_impact')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'wiki_url',
        'image_url',
        'description',
        'dlc',
        'spoil_time',
        'kcal_per_kg',
        'food_gained',
        'slug',
        'sources',
        'food_quality',
        'is_ingredient',
    )
    list_filter = ('is_ingredient',)
    raw_id_fields = ('ingredients',)
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ['name']}


@admin.register(FoodItemSource)
class FoodItemSourceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'wiki_url',
        'image_url',
        'description',
        'slug',
    )
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ['name']}


@admin.register(FoodItemDLC)
class FoodItemDLCAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'wiki_url', 'image_url')
    search_fields = ('name',)


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'ingredient', 'role', 'amount', 'unit')
    list_filter = ('recipe', 'ingredient')
