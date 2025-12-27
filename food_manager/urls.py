from django.urls import path
from .views import RecipeShowcase

urlpatterns = [
    path("foods/", RecipeShowcase.as_view(), name="recipe_showcase"),
]