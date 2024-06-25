# Python imports

# Django imports
from django import forms
from django.shortcuts import redirect

# Local imports
import simulation.config as config
import simulation.scripts.attribute as attribute
import simulation.scripts.badge as badge
from players.models import Player


# Form for creating a player
class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = [
            "first_name",
            "last_name",
            "position",
            "number",
            "country",
            "college",
        ]
        labels = {
            "first_name": "First Name",
            "last_name": "Last Name",
            "position": "Position",
            "number": "Number",
            "country": "Country",
            "college": "College",
        }
        help_texts = {
            "first_name": "So, what's your name, pal?",
            "last_name": "Alright, and your last name?",
            "position": "What position favors ya?",
            "number": "Decent... what number do you want?",
            "country": "And where are you from?",
            "college": "Full ride? Where at?",
        }
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "position": forms.Select(attrs={"class": "form-control"}),
            "number": forms.NumberInput(attrs={"class": "form-control"}),
            "country": forms.Select(attrs={"class": "form-control"}),
            "college": forms.Select(attrs={"class": "form-control"}),
        }


class UpgradeForm(forms.Form):
    def __init__(self, *args, **kwargs):

        # Get the player instance from the keyword arguments & call the parent class' __init__ method
        player = kwargs.pop("player", None)
        banned = {
            "attributes": attribute.physical_attributes + ["Intangibles"],
            "badges": [],
        }
        super().__init__(*args, **kwargs)

        # fmt: off
        if player:
            # Add attribute fields to the form
            for key, value in player.attributes.items():
                if not key in banned["attributes"]:
                    self.fields[key] = forms.IntegerField(
                        label=key,
                        initial=value,
                        widget=forms.NumberInput(
                            attrs={
                                "style": "font-size: 1rem;",
                                "data_type": "attribute",
                                "data-original": value,
                                "class": "attribute-value text-light border-0 bg-transparent p-0 m-0 text-body",
                                "min": "0", 
                                "max": "99"
                            }
                        ),
                    )
            # Add badge fields to the form
            for key, value in player.badges.items():
                # Filter out lower badge levels
                badge_labels = config.CONFIG_PLAYER["BADGE_LABELS"]
                filtered_choices = [(value, badge_labels[value])]
                for level, label in badge_labels.items():
                    if level > value:
                        filtered_choices.append((level, label))
                # Add the field to the form
                self.fields[key] = forms.IntegerField(
                    label=key,
                    initial=value,
                    widget=forms.NumberInput(
                        attrs={
                            "style": "font-size: 0.8rem;",
                            "data_type": "badge",
                            "data-original": value,
                            "class": "badge-value text-light border-0 bg-transparent p-0 m-0 text-body",
                            "min": "0", 
                            "max": "4"
                        }
                    ),
                )
            # Add tendency choices to the field
            for key, value in player.tendencies.items():
                self.fields[key] = forms.IntegerField(
                    label=key,
                    initial=value,
                    widget=forms.NumberInput(
                        attrs={
                            "style": "font-size: 0.8rem;",
                            "data_type": "tendency",
                            "data-original": value,
                            "class": "tendency-value text-light border-0 bg-transparent p-0 m-0 text-body",
                            "min": "0", 
                            "max": "100"
                        }
                    ),
                )
                # fmt: on
