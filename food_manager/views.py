from django.http import HttpResponseNotFound
from django.core.paginator import Paginator
from django.db.models import Prefetch, Q
from django.shortcuts import render
from food_manager.models import Recipe, RecipeIngredient

# Create your views here.


def prefetch_recipes(
    object_queryset,
):
    processed_data = object_queryset.prefetch_related(
        Prefetch(
            "recipe_ingredients",
            queryset=RecipeIngredient.objects.filter(role="required").select_related(
                "ingredient"
            ),
            to_attr="prefetched_required_ingredients",
        ),
        Prefetch(
            "recipe_ingredients",
            queryset=RecipeIngredient.objects.filter(role="subst").select_related(
                "ingredient"
            ),
            to_attr="prefetched_subst_ingredients",
        ),
        "sources",
        "dlc",
        "ingredients",
        "food_quality",
        "recipe_ingredients",
        "recipe_ingredients__ingredient",
        "recipe_ingredients__ingredient__sources",
        "recipe_ingredients__ingredient__dlc",
        "recipe_ingredients__ingredient__food_quality",
    )
    return processed_data


def default_paginator(object_list, request):
    paginator = Paginator(object_list, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return page_obj


def recipe_display(request):
    context = {}
    if request.method == "GET":
        objects = Recipe.objects.all()
        recipes = prefetch_recipes(objects).order_by("name")
        paginated_data = default_paginator(recipes, request)
        context["recipes"] = paginated_data
        return render(request, "foods/index.html", context=context)

    elif request.method == "POST":
        query = request.POST.get("recipe-search", "")
        if query == "" or query is None:
            objects = Recipe.objects.all()
        else:
            objects = Recipe.objects.filter(
                Q(name__icontains=query) | Q(slug__icontains=query)
            )
        recipes = prefetch_recipes(objects).order_by("name")
        paginated_data = default_paginator(recipes, request)
        context["recipes"] = paginated_data
        return render(request, "partials/recipe-list.html", context=context)
    else:
        return HttpResponseNotFound("Invalid Request")
