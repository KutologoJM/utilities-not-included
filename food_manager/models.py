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

    dlc = models.ForeignKey("FoodItemDLC", on_delete=models.PROTECT)

    spoil_time = models.PositiveIntegerField(null=True, blank=True)
    kcal_per_kg = models.PositiveIntegerField(null=True, blank=True)
    food_gained = models.CharField(max_length=100, blank=True)

    slug = AutoSlugField(unique=True, populate_from='name')

    sources = models.ForeignKey("FoodItemSource", on_delete=models.PROTECT)
    food_quality = models.ForeignKey("FoodQuality", on_delete=models.PROTECT)

    is_ingredient = models.BooleanField(default=False)
    ingredients = models.ManyToManyField("self", blank=True, through="RecipeIngredient", related_name="used_in",
                                         symmetrical=False)

    @property
    def required_ingredients(self):
        return self.recipe_ingredients.filter(
            role=RecipeIngredient.Roles.REQUIRED
        )

    @property
    def substitutable_ingredients(self):
        return self.recipe_ingredients.filter(
            role=RecipeIngredient.Roles.SUBSTITUTABLE
        )

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
    name = models.CharField(max_length=50)
    wiki_url = models.URLField()
    image_url = models.URLField()


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

    def __str__(self):
        return f"{self.amount} {self.unit} of {self.ingredient.name} for {self.recipe.name}"
