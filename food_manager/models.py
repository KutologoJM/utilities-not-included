from django.db import models
from django_extensions.db.fields import AutoSlugField
from django.db.models import Prefetch


# Create your models here.


class FoodQuality(models.Model):
    quality = models.CharField(max_length=10, unique=True)
    morale_impact = models.IntegerField()

    def __str__(self):
        if self.morale_impact > 0:
            morale_impact = f"+{self.morale_impact}"
        else:
            morale_impact = self.morale_impact
        return f"{self.quality} [{morale_impact}]"

    class Meta:
        verbose_name = "Food Quality"
        verbose_name_plural = "Food Qualities"


class Recipe(models.Model):
    class Units(models.TextChoices):
        KCAL = "kcal", "Kcal"
        KILOGRAMS = "kg", "Kilograms"
        UNITS = "units", "Units"
        GRAMS = "g", "Grams"

    name = models.CharField(max_length=50, unique=True, db_index=True)
    wiki_url = models.URLField(blank=True)  # null = True not recommended
    image_url = models.URLField(blank=True)
    description = models.TextField(blank=True)

    dlc = models.ForeignKey("FoodItemDLC", on_delete=models.PROTECT)

    spoil_time = models.PositiveIntegerField(null=True, blank=True)
    kcal_per_kg = models.PositiveIntegerField(null=True, blank=True)
    food_gained = models.CharField(max_length=100, blank=True)

    slug = AutoSlugField(unique=True, populate_from='name', db_index=True)

    sources = models.ForeignKey("FoodItemSource", on_delete=models.PROTECT)
    food_quality = models.ForeignKey("FoodQuality", on_delete=models.PROTECT, null=True)

    is_ingredient = models.BooleanField(default=False)
    ingredients = models.ManyToManyField("self", blank=True, through="RecipeIngredient", related_name="used_in",
                                         symmetrical=False)

    @property
    def required_ingredients(self):
        # Use the prefetched list if available, fallback to DB query
        return getattr(self, 'prefetched_required_ingredients',
                       self.recipe_ingredients.filter(role=RecipeIngredient.Roles.REQUIRED))

    @property
    def substitutable_ingredients(self):
        # Use the prefetched list if available, fallback to DB query
        return getattr(self, 'prefetched_required_ingredients',
                       self.recipe_ingredients.filter(role=RecipeIngredient.Roles.SUBSTITUTABLE))

    class Meta:
        verbose_name = "Recipe"
        verbose_name_plural = "Recipes"

    def __str__(self):
        return self.name


class FoodItemSource(models.Model):
    name = models.CharField(max_length=50, unique=True)
    wiki_url = models.URLField(blank=True)
    image_url = models.URLField(blank=True)
    description = models.TextField(blank=True)

    slug = AutoSlugField(unique=True, populate_from='name')

    def __str__(self):
        return self.name


class FoodItemDLC(models.Model):
    name = models.CharField(max_length=50, unique=True)
    wiki_url = models.URLField()
    image_url = models.URLField()

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    class Roles(models.TextChoices):
        REQUIRED = "required", "Required"
        SUBSTITUTABLE = "subst", "Substitutable"

    class Units(models.TextChoices):
        KCAL = "kcal", "Kcal"
        KG = "kg", "Kg"
        UNITS = "units", "Units"
        GRAMS = "g", "Grams"

    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE, related_name="recipe_ingredients")
    ingredient = models.ForeignKey("Recipe", on_delete=models.CASCADE, related_name="ingredient_in")
    role = models.CharField(choices=Roles, default=Roles.REQUIRED, max_length=10)
    amount = models.PositiveIntegerField(default=0)
    unit = models.CharField(choices=Units, default=Units.KCAL, max_length=10)

    class Meta:
        verbose_name = "Recipe Ingredient"
        verbose_name_plural = "Recipe Ingredients"
        unique_together = ("recipe", "ingredient")

    def __str__(self):
        return f"{self.amount} {self.unit} of {self.ingredient.name} for {self.recipe.name}"


class Colony(models.Model):
    name = models.CharField(max_length=50, unique=True)
    difficulty = models.PositiveIntegerField(default=1000) # placeholder logic
    population = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class BlueprintFoods(models.Model):
    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE)
    blueprint = models.ForeignKey("Blueprint", on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.amount} x {self.recipe.name} for {self.blueprint.name}"

class Blueprint(models.Model):
    colony = models.ForeignKey("Colony", on_delete=models.PROTECT)
    name = models.CharField(max_length=50, unique=True)
    num_of_duplicants = models.PositiveIntegerField(default=0)
    survivable_cycles = models.PositiveIntegerField(default=0)
    selected_foods = models.ManyToManyField(
        "Recipe", through="BlueprintFoods"
    )

    def __str__(self):
        return f"{self.name} for {self.colony.name}"

"""
class Blueprint(models.Model):
    class Goals(models.TextChoices):
        support_x_dupes = "supp_x_dupes", "Support x dupes"
        last_x_cycles = "last_x_cycles", "Last x cycles"
    blueprint_name = models.CharField(max_length=50, unique=True)
    colony_name = models.CharField(max_length=50)
    num_of_duplicants = models.PositiveIntegerField(default=0)
    hunger_setting = models.ForeignKey("HungerLevels", on_delete=models.PROTECT)
    current_goal = models.CharField(choices=Goals, default=Goals.last_x_cycles, max_length=20)
    chosen_foods = models.TextField(blank=True) # todo change to a m2m field with a through table for amounts

    @property
    def daily_kcal_needed(self):
        # for ingredient in chosen ingredients, num dupes x difficulty
        return 0

    @property
    def kcal_produced(self):
        # for ingredient in chosen ingredients, ingredient.you get x num of chosen ingredient, ?move to through table
        return 0

    @property
    def num_of_survivable_cycles(self):
        # num of " cycles = food produced / num of dupes * hunger difficulty
        return 0


class HungerLevels(models.Model):
    level = models.CharField(max_length=50)
    kcal_required = models.PositiveIntegerField(default=1000)


class GameSettings(models.Model):
    class GameModePresets(models.TextChoices):
        SURVIVAL = "survival", "Survival"
        NO_SWEAT = "no sweat", "No sweat"
        CUSTOM ="custom", "Custom"
    class AsteroidStyles(models.TextChoices):
        CLASSIC = "classic", "Classic"
        SPACED_OUT ="spaced_out", "Spaced Out"
        THE_LAB = "the-lab", "The Lab"

    preset = models.CharField(max_length=50)

    worldgen_seen = models.PositiveIntegerField(default=0)
    # hunger, durablity, radiation, stress reactions (bool)
    # teleporters(bool), disesase, morale, meteor showers, stress
    # care packaged, demolior impact

    # model for asteroids and major colony / save file

    def __str__(self):
        return self.name
"""