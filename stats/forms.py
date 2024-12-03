# Python imports

# Django imports
from django import forms
from django.shortcuts import redirect

# Local imports
import simulation.config as config
from players.models import Player
from stats.models import Game, PlayerGameStats, TeamGameStats

# PlayerGameStatsForm
class PlayerGameStatsForm(forms.ModelForm):
    class Meta:
        model = PlayerGameStats
        exclude = [
            "created", 
            "points", 
            "defensive_rebounds", 
            "game_score", 
            "effective_field_goal_percentage", 
            "true_shooting_percentage", 
            "turnover_percentage"
        ]

# GameForm
class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        exclude = ["created"]

    player_stats = forms.formset_factory(PlayerGameStatsForm, extra=10)
