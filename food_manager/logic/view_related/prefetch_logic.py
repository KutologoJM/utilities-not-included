from django.db.models import Prefetch
from food_manager.models import RecipeIngredient


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