from django.shortcuts import render
from django.core.paginator import Paginator
from food_manager.models import Recipe, RecipeIngredient, Blueprint
from django.db.models import Q, Prefetch
from .forms import FoodForm


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
    recipes = prefetch_all_recipes().order_by('name')

    paginator = Paginator(recipes, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context['recipes'] = page_obj
    context['page_obj'] = page_obj
    context['form'] = FoodForm()

    return render(request, 'foods/test.html', context)


def search_recipes(request):
    context = {}
    query = request.GET.get('recipe-search', '')
    if query == '' or query is None:
        recipes = prefetch_all_recipes().order_by('name')

        paginator = Paginator(recipes, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['recipes'] = page_obj
        context['page_obj'] = page_obj

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
        ).order_by('name')

        paginator = Paginator(recipes, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['recipes'] = page_obj
        context['page_obj'] = page_obj

    return render(request, "partials/recipe-list.html", context=context)


def blueprint_display(request):
    context = {}
    context['blueprints'] = Blueprint.objects.all()
    return render(request, 'foods/blueprint.html', context=context)
