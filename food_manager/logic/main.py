import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "UtilitiesNotIncluded.settings.dev")
django.setup()

from food_manager.models import Recipe


class KcalCalculator:
    def __init__(self, slug, quantity):
        self.total_kcal_produced = 0
        self.kcal_produced = 0
        self.slug = slug
        self.quantity = quantity
        self.recipe = None

    def __str__(self):
        return f"{self.quantity} x {self.recipe.name} produced {self.total_kcal_produced} kcal"

    def __repr__(self):
        return f"slug:{self.slug} quantity:{self.quantity} recipe:{self.recipe.name}"

    def get_recipe_instance(self):
        self.recipe = Recipe.objects.get(slug=self.slug)
        return self.recipe

    def calculate_total_kcal_produced(self):
        recipe: Recipe = self.get_recipe_instance()
        self.kcal_produced = int(recipe.food_gained.split("kcal")[0])
        self.total_kcal_produced = self.kcal_produced * self.quantity
        return self.total_kcal_produced


user_provided_data = [
    {
        "slug": "frost-burger",
        "quantity": 5,
    },
    {
        "slug": "veggie-poppers",
        "quantity": 4,
    },
    {
        "slug": "tender-brisket",
        "quantity": 3,
    },
]  # a list of user chosen recipes

results = []

for data in user_provided_data:
    slug_ = data["slug"]
    quantity_ = data["quantity"]

    object_ = KcalCalculator(slug_, quantity_)
    object_.calculate_total_kcal_produced()
    results.append(object_)
    print(object_.recipe.name)
    print(object_.total_kcal_produced)
    print(object_)

print(results)
