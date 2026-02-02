from django import forms
from food_manager.models import Recipe


class FoodForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            "name",
            "wiki_url",
            "image_url",
            "description",
            "dlc",
            "spoil_time",
            "kcal_per_kg",
            "food_gained",
            "sources",
            "food_quality",
            "is_ingredient",
            "ingredients",
        ]
