from django.contrib import admin
from food_manager import models
# Register your models here.
admin.site.register(models.Recipe)
admin.site.register(models.FoodQuality)
admin.site.register(models.RecipeIngredient)
admin.site.register(models.FoodItemSource)
admin.site.register(models.FoodItemDLC)

admin.site.register(models.BlueprintFoods)
admin.site.register(models.Blueprint)