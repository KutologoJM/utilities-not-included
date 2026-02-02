from django import forms
from colony_manager.models import Colony


class CreateColonyForm(forms.ModelForm):
    class Meta:
        model = Colony
        fields = [
            "name",
            "stress_reactions",
            "sandbox_mode",
            "teleporters",
            "care_packages",
            "save_to_cloud",
            "preset",
            "asteroid_style",
            "hunger",
            "durability",
            "radiation",
            "disease",
            "morale",
            "meteorshowers",
            "stress",
            "demolior_impact",
        ]
