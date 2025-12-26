from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Recipe)
admin.site.register(models.FoodQuality)
admin.site.register(models.RecipeIngredient)
admin.site.register(models.FoodItemSource)