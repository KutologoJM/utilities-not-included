from django.shortcuts import render
from food_manager.models import Recipe
from django.db.models import Q

# Create your views here.

def index(request):
    context = {}
    recipes = Recipe.objects.all().order_by('-id')
    context['recipes'] = recipes
    return render(request, 'foods/recipes.html', context)

def search_recipes(request):
    query = request.GET.get('search', '')
    order_by = request.GET.get('order_by', '')

    # use the query to filter recipes by name or slug
    recipes = Recipe.objects.filter(
        Q(name__icontains=query) | Q(slug__icontains=query)
    )
    recipes.order_by(order_by)
    return render(request, "partials/recipe-list.html", {'recipes': recipes})