import os
import django
import json
from django.utils.text import slugify

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "UtilitiesNotIncluded.settings.dev")
django.setup()

from food_manager.models import (
    FoodQuality,
    FoodItemDLC,
    FoodItemSource,
    Recipe,
)  # noqa: E402


def filter_food_quality(data):
    data = data["food_quality"]
    quality = data["quality"]
    morale_impact: str = data["morale_impact"]
    morale_impact = morale_impact.strip("+")
    return quality, int(morale_impact)


def populate_dlc_model(data):
    if (
        data["dlc_name"] is None
        or data["dlc_wiki_url"] is None
        or data["dlc_image_url"] is None
    ):
        name = "Base Game"
        wiki_url = "https://oxygennotincluded.wiki.gg/"
        image_url = "https://oxygennotincluded.wiki.gg/images/Logo.png"
    else:
        name = data["dlc_name"]
        wiki_url = f"https://oxygennotincluded.wiki.gg{data['dlc_wiki_url']}"
        image_url = f"https://oxygennotincluded.wiki.gg{data['dlc_image_url']}"
    dlc, created = FoodItemDLC.objects.get_or_create(
        name=name,
        defaults={
            "name": name,
            "wiki_url": wiki_url,
            "image_url": image_url,
        },
    )
    if created:
        return f"Created new dlc element. DLC: {dlc.name}"
    else:
        return f"DLC already exists. DLC: {dlc.name}"


def populate_recipe_ingredients_model(data):
    pass


def populate_sources_model(data):
    for source in data["sources"]:
        name = source["name"]
        wiki_url = f"https://oxygennotincluded.wiki.gg{source['wiki_url']}"
        image_url = f"https://oxygennotincluded.wiki.gg{source['image_url']}"
        description = ""
        print(name, wiki_url, image_url, description)
        obj, created = FoodItemSource.objects.get_or_create(
            name=name,
            defaults={
                "name": name,
                "wiki_url": wiki_url,
                "image_url": image_url,
            },
        )
        if created:
            return f"Created new source element. Source: {obj.name}"
        else:
            return f"Source already exists. Source: {obj.name}"


def populate_food_quality_model(data):
    if data["food_quality"]:
        quality, morale_impact = filter_food_quality(data)
    else:
        return None
    food_quality, created = FoodQuality.objects.get_or_create(
        quality=quality,
        defaults={
            "quality": quality,
            "morale_impact": morale_impact,
        },
    )
    if created:
        return f"Created new food quality element. Food quality: {food_quality.quality}"
    else:
        return f"Food quality already exists. Food quality: {food_quality.quality}"


def filter_food_gained(data):
    total_food_gained = ""
    if len(data) > 1:
        total_food_gained = f"{data[0]} - {data[1]}"
    else:
        total_food_gained = data[0]
    return total_food_gained


def populate_recipe_model(data):
    name = data["name"]
    if name == "Surf'n'Turf":
        name = "Surf n Turf"
    print(f"Executing for {name} ")
    wiki_url = f"https://oxygennotincluded.wiki.gg{data['wiki_url']}"
    image_url = f"https://oxygennotincluded.wiki.gg{data['image_url']}"
    description = ""
    is_ingredient = False
    spoil_time = data["spoil_time"]
    kcal_per_kg = data["kcal_per_kg"]

    food_gained = filter_food_gained(data["food_gained"])

    if data["dlc_name"] is not None:
        dlc = FoodItemDLC.objects.get(name=data["dlc_name"])
    else:
        dlc = FoodItemDLC.objects.get(name="Base Game")

    if data["food_quality"] is not None:
        quality, morale_impact = filter_food_quality(data)
        food_quality = FoodQuality.objects.get(quality=quality)
    else:
        food_quality = None

    if data["sources"] is not None:
        sources = data["sources"]
        compiled_sources = []
        for source in sources:
            source_name = source["name"]
            obj, created = FoodItemSource.objects.get_or_create(
                name=source_name,
                defaults={
                    "name": source_name,
                    "wiki_url": f"https://oxygennotincluded.wiki.gg{wiki_url}",
                    "image_url": f"https://oxygennotincluded.wiki.gg{image_url}",
                    "description": "",
                },
            )
            compiled_sources.append(FoodItemSource.objects.get(name=source_name))
        sources = compiled_sources[0]
    else:
        sources = None

    recipe, created = Recipe.objects.get_or_create(
        slug=slugify(name),
        defaults={
            "name": name,
            "wiki_url": wiki_url,
            "image_url": image_url,
            "description": description,
            "is_ingredient": is_ingredient,
            "spoil_time": spoil_time,
            "kcal_per_kg": kcal_per_kg,
            "food_gained": food_gained,
            "sources": sources,
            "food_quality": food_quality,
            "dlc": dlc,
        },
    )
    if created:
        return f"Created new recipe element. Recipe: {recipe.name}"
    else:
        return f"Recipe already exists. Recipe: {recipe.name}"


with open("compiled_food_items.json") as json_file:
    food_items = json.load(json_file)
    for food_item in food_items:
        # print(slugify(food_item['name']))
        # print(food_item['food_gained'])
        # print(populate_sources_model(food_item))
        # print(populate_dlc_model(food_item))
        # print(populate_food_quality_model(food_item))
        # print(filter_food_gained(food_item["food_gained"]))
        print(populate_recipe_model(food_item))
