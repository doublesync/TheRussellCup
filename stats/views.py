# Python imports
import json

# Django imports
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.generic.list import ListView

# Local imports
from django.views.generic import TemplateView
from stats.models import Game, TeamGameStats, PlayerGameStats
from players.models import Player
from teams.models import Team
import simulation.statfinder as statfinder

# Create your views here.
def stats_home(request):
    objects = Player.objects.all()
    players = {}
    for player in objects:
        players[player.id] = statfinder.StatFinder(fetch_all_season=True).player_averages(player)
        players[player.id]["full_name"] = f"{player.first_name} {player.last_name}"
    return render(request, "stats/stats_home.html", {"players": players})

# def stats_season(request, id):
#     return HttpResponse(f"S{id} Stats")