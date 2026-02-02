from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from food_manager.logic.view_related.pagination import default_paginator
from food_manager.logic.view_related.prefetch_logic import prefetch_recipes
from food_manager.models import Recipe


# Views begin here

class Index(TemplateView):
    template_name = "pages/fm_index.html"
    extra_context = {}


def search_recipes(request):
    """
    Dual-purpose view. Returns one or all views depending on the search criteria.
    :param request:
    :return:
    """
    context = {}
    if request.method == "GET":
        objects = Recipe.objects.all()
        recipes = prefetch_recipes(objects).order_by("name")
        paginated_data = default_paginator(recipes, request)
        context["recipes"] = paginated_data
        return render(request, "partials/recipe-cards.html", context=context)
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
        return render(request, "partials/recipe-cards.html",
                      context=context)  # todo f" {template}" so that its reusable
    else:
        return HttpResponse("Unsupported Method", status=405)


def calculate_and_render_chosen_recipes(request):
    context = {}
    chosen_recipes = request.session["chosen_recipes"]
    results = []
    sum_total = 0

    from food_manager.logic.view_related.kcal_calculator import KcalCalculator

    for data in chosen_recipes:
        slug: str = data["slug"]
        quantity: int = data["quantity"]
        calculator = KcalCalculator(slug, quantity)
        calculator.calculate_total_kcal_produced()
        results.append(calculator)
        sum_total += calculator.total_kcal_produced

    context["chosen_recipes"] = results
    context["sum_total"] = sum_total

    return render(request, "partials/chosen-recipes.html", context)


def manage_chosen_recipes(request):
    """
    Initializes chosen recipes in session, performs user requested action and calls calculate_and_render_chosen_recipes
    :param request:
    :return:
    """
    if "chosen_recipes" not in request.session:
        request.session["chosen_recipes"] = []
    chosen_recipes = request.session["chosen_recipes"]

    # todo give feedback for when user tries to add the same food+quantity
    # current behaviour blocks it from being added

    if request.method == "POST":
        # todo replace with a form
        action: str = request.POST.get("action")
        slug: str = request.POST.get("slug")
        quantity: int = int(request.POST.get("quantity"))
        food_dict: dict = {"slug": slug, "quantity": quantity}

        if action == "remove" and food_dict in chosen_recipes:
            chosen_recipes.remove(food_dict)
        elif action == "add" and food_dict not in chosen_recipes:
            chosen_recipes.append(food_dict)
        else:
            pass
        request.session.modified = True

        return redirect("food_manager:calculate_and_render_chosen_recipes")  # todo turn into a var that htmx can send

    else:
        return HttpResponse("Unsupported Method", status=403)
