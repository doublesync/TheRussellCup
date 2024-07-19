# Python imports
import json

# Django imports
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import render

# Local imports
from stats.models import Season
import simulation.statfinder as statfinder

# Create your views here.
def stats_home(request):
    finder = statfinder.StatFinder(fetch_all_season=True)
    players = finder.all_player_averages()
    standings = finder.league_standings()
    performances = statfinder.get_season_performances()
    return render(request, "stats/stats_home.html", {"players": players, "standings": standings, "performances": performances})

# A function that sorts the players by a given stat
def sort_by_stat(request, stat):
    if request.method == "POST":
        # Get the averages for each player
        players = statfinder.StatFinder(fetch_all_season=True).all_player_averages()
        # Sort by the stat & make a dictionary of players
        order_type = request.POST.get("order-type")
        reverse_order = False if order_type == "asc" else True
        sorted_players = {k: v for k, v in sorted(players.items(), key=lambda item: item[1][stat], reverse=reverse_order)}
        # Render to string
        fragment_html = render_to_string("stats/fragments/list_fragment.html", {"players": sorted_players})
        return HttpResponse(fragment_html)
    
# A function that returns the records page
def records(request):
    season = Season.objects.filter(current_season=True).first()
    return render(request, "stats/records.html", {"season": season})

# A function that returns the performances page
def performances(request):
    performances = statfinder.get_season_performances()
    return render(request, "stats/performances.html", {"performances": performances})