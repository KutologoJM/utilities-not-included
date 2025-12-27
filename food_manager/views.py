from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Recipe


# Create your views here.
class RecipeShowcase(ListView):
    model = Recipe
    template_name = "foods/recipe_list.html"
    context_object_name = "recipes"
    queryset = Recipe.objects.filter(is_ingredient=False)
