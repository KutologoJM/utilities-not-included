from django.db import models
from django_extensions.db.fields import AutoSlugField


# Create your models here.

class FoodQuality(models.Model):
    quality = models.CharField(max_length=10)
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

    name = models.CharField(max_length=50, unique=True)
    wiki_url = models.URLField(blank=True)  # null = True not recommended
    image_url = models.URLField(blank=True)
    description = models.TextField(blank=True)

    dlc_name = models.CharField(max_length=50, blank=True)
    dlc_wiki_url = models.URLField(blank=True)
    dlc_image_url = models.URLField(blank=True)

    spoil_time = models.PositiveIntegerField(null=True, blank=True)
    kcal_per_kg = models.PositiveIntegerField(null=True, blank=True)
    food_gained = models.PositiveIntegerField()
    unit = models.CharField(choices=Units, default=Units.KCAL, max_length=10)

    slug = AutoSlugField(unique=True, populate_from='name')

    sources = models.ManyToManyField("FoodItemSource", blank=True)
    food_quality = models.ForeignKey("FoodQuality", on_delete=models.PROTECT, related_name="recipe")

    is_ingredient = models.BooleanField(default=False)
    ingredients = models.ManyToManyField("self",  blank=True, through="RecipeIngredient", related_name="used_in", symmetrical=False)

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


class RecipeIngredient(models.Model):
    class Roles(models.TextChoices):
        MAIN = "main", "Main"
        ALTERNATE = "alt", "Alternate"

    class Units(models.TextChoices):
        KCAL = "kcal", "Kcal"
        KG = "kg", "Kg"
        UNITS = "units", "Units"
        GRAMS = "g", "Grams"

    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE, related_name="recipe_ingredients")
    ingredient = models.ForeignKey("Recipe", on_delete=models.CASCADE, related_name="ingredient_in")
    role = models.CharField(choices=Roles, default=Roles.MAIN, max_length=10)
    amount = models.PositiveIntegerField(default=0)
    unit = models.CharField(choices=Units, default=Units.KCAL, max_length=10)

    class Meta:
        verbose_name = "Recipe Ingredient"
        verbose_name_plural = "Recipe Ingredients"

    def __str__(self):
        return f"{self.amount} {self.unit} of {self.ingredient.name} for {self.recipe.name}"


"""
ingredient.recipe_links.all()     # All recipes using this ingredient
recipe.ingredient_links.all()     # All ingredients in this recipe

"""
