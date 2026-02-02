from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from colony_manager.models import (
    Colony,
    Hunger,
    Durability,
    Radiation,
    Disease,
    Morale,
    MeteorShowers,
    Stress,
    DemoliorImpact,
    Planetoid,
    Blueprint,
)
from colony_manager.forms import CreateColonyForm
from food_manager.logic.view_related.pagination import default_paginator
from food_manager.logic.view_related.prefetch_logic import prefetch_recipes
from food_manager.models import Recipe


class Index(LoginRequiredMixin,TemplateView):
    template_name = "pages/cm_index.html"
    extra_context = {}


@login_required
def create_colony(request):
    """
    Used to create a new colony
    :param request:
    :return:
    """

    form = CreateColonyForm(request.POST)
    if form.is_valid():
        return render(
            request, "partials/colony_creation_success.html", {"form": form}
        )
    return HttpResponse('Form is not valid')


@login_required
def edit_colony(request, colony):
    """
    Used to edit an existing colony
    :param request:
    :return:
    """
    context = {}

    return render(request, "pages/colony_editor.html", context=context)


@login_required
def planetoid_index(request, colony):
    user = request.user
    context = {}  # noqa
    if user.is_staff or user.is_superuser:
        context["planetoids"] = Planetoid.objects.all()
    else:
        context["planetoids"] = Planetoid.objects.filter(user=user)
    return render(request, "pages/planetoid_index.html", context)


@login_required
def create_planetoid(request, colony):
    """
    Used to create a new planetoid
    :param request:
    :return:
    """
    context = {}
    return render(request, "partials/planetoid_creation_success.html", context=context)


@login_required
def edit_planetoid(request, colony, planetoid):
    """
    Used to edit an existing planetoid
    :param request:
    :return:
    """
    return render(request, "pages/planetoid_editor.html")


@login_required
def blueprint_index(request, colony, planetoid):
    context = {}
    filtered_blueprints = Blueprint.objects.filter(planetoid__slug=planetoid)
    context["blueprints"] = filtered_blueprints
    return render(request, "pages/blueprint_index.html", context)


@login_required
def blueprint_maker(request, colony, planetoid):
    context = {}
    # request.session["chosen_foods"] = [] used in dev to quickly clear session
    if request.method == "GET":
        objects = Recipe.objects.all()
        recipes = prefetch_recipes(objects).order_by("name")
        paginated_data = default_paginator(recipes, request)
        context["recipes"] = paginated_data
        return render(request, "pages/blueprint_maker.html", context=context)
    return HttpResponse('Not implemented')


@login_required
def create_blueprint(request):
    data = request.session["chosen_recipes"]
    request.session["chosen_recipes"] = []
    return redirect("colony_manager:blueprint-creation-success")


@login_required
def blueprint_creation_success(request):
    context = {}
    return render(request, "partials/blueprint_creation_success.html", context=context)
