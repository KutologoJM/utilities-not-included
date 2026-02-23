from django.contrib import admin

from .models import Hunger, Durability, Radiation, Disease, Morale, MeteorShowers, Stress, DemoliorImpact, Colony, Planetoid, Blueprint, BlueprintFoods


@admin.register(Hunger)
class HungerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'kcal_required')
    search_fields = ('name',)


@admin.register(Durability)
class DurabilityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'rate_of_decay')
    search_fields = ('name',)


@admin.register(Radiation)
class RadiationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Disease)
class DiseaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Morale)
class MoraleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(MeteorShowers)
class MeteorShowersAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Stress)
class StressAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'stress_rate')
    search_fields = ('name',)


@admin.register(DemoliorImpact)
class DemoliorImpactAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Colony)
class ColonyAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'name',
        'slug',
        'stress_reactions',
        'sandbox_mode',
        'teleporters',
        'care_packages',
        'save_to_cloud',
        'preset',
        'asteroid_style',
        'hunger',
        'durability',
        'radiation',
        'disease',
        'morale',
        'meteorshowers',
        'stress',
        'demolior_impact',
    )
    list_filter = (
        'user',
        'stress_reactions',
        'sandbox_mode',
        'teleporters',
        'care_packages',
        'save_to_cloud',
        'hunger',
        'durability',
        'radiation',
        'disease',
        'morale',
        'meteorshowers',
        'stress',
        'demolior_impact',
    )
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ['name']}


@admin.register(Planetoid)
class PlanetoidAdmin(admin.ModelAdmin):
    list_display = ('id', 'colony', 'name', 'dupe_population', 'slug')
    list_filter = ('colony',)
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ['name']}


@admin.register(Blueprint)
class BlueprintAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'planetoid',
        'name',
        'supportable_dupes',
        'survivable_cycles',
        'slug',
    )
    list_filter = ('planetoid',)
    raw_id_fields = ('selected_foods',)
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ['name']}


@admin.register(BlueprintFoods)
class BlueprintFoodsAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'blueprint', 'amount')
    list_filter = ('recipe', 'blueprint')