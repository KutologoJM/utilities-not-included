from django.db import models
from django_extensions.db.fields import AutoSlugField

from accounts.models import CustomUser
from food_manager.models import Recipe


# Create your models here.


class Hunger(models.Model):
    name = models.CharField(max_length=100)
    kcal_required = models.PositiveIntegerField(default=1000)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Hunger"
        verbose_name_plural = "Hunger"


class Durability(models.Model):
    name = models.CharField(max_length=100)
    rate_of_decay = models.PositiveIntegerField(default=10)  # percentage

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Durability"
        verbose_name_plural = "Durabilities"


class Radiation(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Radiation"
        verbose_name_plural = "Radiation"


class Disease(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Disease"
        verbose_name_plural = "Diseases"


class Morale(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Morale"
        verbose_name_plural = "Morales"


class MeteorShowers(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Meteor Showers"
        verbose_name_plural = "Meteor Showers"


class Stress(models.Model):
    name = models.CharField(max_length=100)
    stress_rate = models.IntegerField(default=0)  # percentage

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Stress"
        verbose_name_plural = "Stress"


class DemoliorImpact(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Demolior Impact"
        verbose_name_plural = "Demolior Impacts"


class Colony(models.Model):
    class GameModePresets(models.TextChoices):
        SURVIVAL = "survival", "Survival"
        NO_SWEAT = "no-sweat", "No sweat"

    class AsteroidStyles(models.TextChoices):
        CLASSIC = "classic", "Classic"
        SPACED_OUT = "spaced_out", "Spaced Out"
        THE_LAB = "the-lab", "The Lab"

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = AutoSlugField(unique=True, populate_from="name", db_index=True)

    stress_reactions = models.BooleanField(default=True)
    sandbox_mode = models.BooleanField(default=False)
    teleporters = models.BooleanField(default=False)
    care_packages = models.BooleanField(default=True)
    save_to_cloud = models.BooleanField(default=False)

    preset = models.CharField(
        choices=GameModePresets, max_length=100, default=GameModePresets.SURVIVAL
    )
    asteroid_style = models.CharField(
        choices=AsteroidStyles, max_length=100, default=AsteroidStyles.CLASSIC
    )

    hunger = models.ForeignKey("Hunger", on_delete=models.CASCADE)
    durability = models.ForeignKey("Durability", on_delete=models.CASCADE)
    radiation = models.ForeignKey("Radiation", on_delete=models.CASCADE)
    disease = models.ForeignKey("Disease", on_delete=models.CASCADE)
    morale = models.ForeignKey("Morale", on_delete=models.CASCADE)
    meteorshowers = models.ForeignKey("MeteorShowers", on_delete=models.CASCADE)
    stress = models.ForeignKey("Stress", on_delete=models.CASCADE)
    demolior_impact = models.ForeignKey(
        "DemoliorImpact", on_delete=models.CASCADE, null=True
    )

    def __str__(self):
        return f"Colony: {self.name}"

    class Meta:
        verbose_name = "Colony"
        verbose_name_plural = "Colonies"


class Planetoid(models.Model):
    colony = models.ForeignKey("Colony", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    dupe_population = models.PositiveIntegerField(default=0)
    slug = AutoSlugField(unique=True, populate_from="name", db_index=True)

    def __str__(self):
        return f"{self.name} in {self.colony.name}"

    class Meta:
        verbose_name = "Planetoid"
        verbose_name_plural = "Planetoids"


class Blueprint(models.Model):
    planetoid = models.ForeignKey("Planetoid", on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True)
    supportable_dupes = models.PositiveIntegerField(default=0)
    survivable_cycles = models.PositiveIntegerField(default=0)
    selected_foods = models.ManyToManyField(Recipe, through="BlueprintFoods")
    slug = AutoSlugField(unique=True, populate_from="name", db_index=True)

    def __str__(self):
        return f"{self.name} for {self.planetoid.name}"


class BlueprintFoods(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    blueprint = models.ForeignKey("Blueprint", on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.amount} x {self.recipe.name} for {self.blueprint.name}"

    class Meta:
        verbose_name = "Blueprint Food"
        verbose_name_plural = "Blueprint Foods"
