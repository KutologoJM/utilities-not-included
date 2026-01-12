from django.shortcuts import render
from food_manager.models import Recipe, RecipeIngredient
from django.db.models import Q, Prefetch


# Create your views here.

def prefetch_all_recipes():
    data = Recipe.objects.all().prefetch_related(
        Prefetch(
            'recipe_ingredients',
            queryset=RecipeIngredient.objects.filter(role='required').select_related('ingredient'),
            to_attr='prefetched_required_ingredients'
        ),
        Prefetch(
            'recipe_ingredients',
            queryset=RecipeIngredient.objects.filter(role='subst').select_related('ingredient'),
            to_attr='prefetched_subst_ingredients'
        ),
        'sources',
        'dlc',
        'ingredients',
        'food_quality',
        'recipe_ingredients',
        'recipe_ingredients__ingredient',
        'recipe_ingredients__ingredient__sources',
        'recipe_ingredients__ingredient__dlc',
        'recipe_ingredients__ingredient__food_quality',
    )
    return data


def index(request):
    context = {}
    recipes = prefetch_all_recipes()
    context['recipes'] = recipes
    return render(request, 'foods/recipes.html', context)


def search_recipes(request):
    context = {}
    query = request.GET.get('search', '')
    if query == '' or query is None:
        recipes = prefetch_all_recipes()
        context['recipes'] = recipes
    else:
        # use the query to filter recipes by name or slug
        recipes = Recipe.objects.filter(
            Q(name__icontains=query) | Q(slug__icontains=query)
        ).prefetch_related(
            Prefetch(
                'recipe_ingredients',
                queryset=RecipeIngredient.objects.filter(role='required').select_related('ingredient'),
                to_attr='prefetched_required_ingredients'
            ),
            Prefetch(
                'recipe_ingredients',
                queryset=RecipeIngredient.objects.filter(role='subst').select_related('ingredient'),
                to_attr='prefetched_subst_ingredients'
            ),
            'sources',
            'dlc',
            'ingredients',
            'food_quality',
            'recipe_ingredients',
            'recipe_ingredients__ingredient',
            'recipe_ingredients__ingredient__sources',
            'recipe_ingredients__ingredient__dlc',
            'recipe_ingredients__ingredient__food_quality',
        )
        context['recipes'] = recipes
    return render(request, "partials/recipe-list.html", context=context)
