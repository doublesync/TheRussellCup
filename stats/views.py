# Python imports
import json

# Django imports
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

# Local imports
from django.views.generic import TemplateView
from stats.models import Game, TeamGameStats, PlayerGameStats
from players.models import Player
from teams.models import Team
import simulation.statfinder as statfinder

# Create your views here.

def stats_player(request, id):
    player = Player.objects.get(pk=id)
    game_averages = statfinder.StatFinder().player_averages(player)
    game_totals = statfinder.StatFinder().player_totals(player)
    return JsonResponse({"Averages": game_averages, "Totals": game_totals})

def stats_teams(request, id):
    team = Team.objects.get(pk=id)
    game_averages = statfinder.StatFinder(fetch_all_season=True).team_averages(team)
    game_totals = statfinder.StatFinder(fetch_all_season=True).team_totals(team)
    game_averages_dump = json.loads(json.dumps(game_averages, indent=4, sort_keys=True, default=str))
    game_totals_dump = json.loads(json.dumps(game_totals, indent=4, sort_keys=True, default=str))
    # we need these parameters in our jsonresponse : indent=4, sort_keys=True, default=str
    return JsonResponse({"Averages": game_averages_dump, "Totals": game_totals_dump})
    # Datetime field comes out as P0DT00H15M26S, why?

# def stats_home(request):
#     return HttpResponse("Stats Home")

# def stats_list(request):
#     return HttpResponse("Stats List")

# def stats_season(request, id):
#     return HttpResponse(f"S{id} Stats")