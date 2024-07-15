# Python imports
import json

# Django imports
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.generic.list import ListView
from django.template.loader import render_to_string

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

# A function that sorts the players by a given stat
def sort_by_stat(request, stat):
    objects = Player.objects.all()
    players = {}
    for player in objects:
        players[player.id] = statfinder.StatFinder(fetch_all_season=True).player_averages(player)
        players[player.id]["full_name"] = f"{player.first_name} {player.last_name}"
    # Sort by the stat & make a dictionary of players key: full_name, value: averages
    # Order type can be ascending or descending
    order_type = request.GET.get("order-type")
    reverse_order = True if order_type == "asc" else False
    # Before sorting, set any None values to 0
    for player in players:
        if players[player][stat] is None:
            players[player][stat] = 0
    sorted_players = {k: v for k, v in sorted(players.items(), key=lambda item: item[1][stat], reverse=reverse_order)}
    # Render to string
    fragment_html = render_to_string("stats/fragments/list_fragment.html", {"players": sorted_players})
    return HttpResponse(fragment_html)