# Python imports

# Django imports
from django import forms

# Local imports
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
