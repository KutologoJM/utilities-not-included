from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
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


# Create your views here.
@login_required
def colony_index(request):
    user = request.user
    context = {}  # noqa
    if user.is_staff or user.is_superuser:
        context["colonies"] = Colony.objects.all()
    else:
        context["colonies"] = Colony.objects.filter(user=user)
    default_hunger = Hunger.objects.get(name="Default")
    default_durability = Durability.objects.get(name="Default")
    default_radiation = Radiation.objects.get(name="Default")
    default_disease = Disease.objects.get(name="Default")
    default_morale = Morale.objects.get(name="Default")
    default_meteorshowers = MeteorShowers.objects.get(name="Default")
    default_stress = Stress.objects.get(name="Default")
    default_demolior_impact = DemoliorImpact.objects.get(name="Default")

    form = CreateColonyForm(
        initial={
            "user": request.user,
            "name": "Placeholder",
            "stress_reaction": True,
            "sandbox_mode": False,
            "teleporters": False,
            "care_packages": True,
            "save_to_cloud": False,
            "hunger": default_hunger,
            "durability": default_durability,
            "radiation": default_radiation,
            "disease": default_disease,
            "morale": default_morale,
            "meteorshowers": default_meteorshowers,
            "stress": default_stress,
            "demolior_impact": default_demolior_impact,
        }
    )
    context["form"] = form
    return render(request, "colony/index.html", context)


@login_required
def colony_creator(request):
    """
    Used to create a new colony
    :param request:
    :return:
    """

    form = CreateColonyForm(request.POST)
    if form.is_valid():
        return render(
            request, "colony/partials/colony_creation_success.html", {"form": form}
        )
    return None


@login_required
def colony_editor(request, colony):
    """
    Used to edit an existing colony
    :param request:
    :return:
    """
    context = {}

    return render(request, "colony/editor.html", context=context)


@login_required
def planetoid_index(request, colony):
    user = request.user
    context = {}  # noqa
    if user.is_staff or user.is_superuser:
        context["planetoids"] = Planetoid.objects.all()
    else:
        context["planetoids"] = Planetoid.objects.filter(user=user)
    return render(request, "planetoid/index.html", context)


@login_required
def planetoid_creator(request, colony):
    """
    Used to create a new planetoid
    :param request:
    :return:
    """
    context = {}
    return render(request, "planetoid/creation_form.html", context=context)


@login_required
def planetoid_editor(request, colony, planetoid):
    """
    Used to edit an existing planetoid
    :param request:
    :return:
    """
    return render(request, "planetoid/editor.html")


def blueprint_index(request, colony, planetoid):
    context = {}
    filtered_blueprints = Blueprint.objects.filter(planetoid__slug=planetoid)
    context["blueprints"] = filtered_blueprints
    return render(request, "blueprints/index.html", context)


def blueprint_calc(request):
    return HttpResponse()
