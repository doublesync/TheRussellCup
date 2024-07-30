# Python imports
import json

# Django imports
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import Q

# Local imports
import simulation.artificial as artificial
from stats.models import Season, Game, PlayerGameStats, TeamGameStats
import simulation.statfinder as statfinder
from django_table_sort.table import TableSort

# Create your views here.
    
# A function that returns the 'player_averages' page
def player_averages(request):
    finder = statfinder.StatFinder(all_season=True)
    players = finder.all_player_averages()
    return render(request, "stats/player_averages.html", {"players": players})

# A function that returns the 'team_averages' page
def stats_home(request):
    finder = statfinder.StatFinder(all_season=True)
    standings = finder.league_standings()
    season = Season.objects.filter(current_season=True).first()
    storylines = season.current_storylines
    return render(request, "stats/stats_home.html", {"standings": standings, "storylines": storylines})

# A function that sorts the players by a given stat
def sort_by_stat(request, stat):
    if request.method == "POST":
        # Get the averages for each player
        players = statfinder.StatFinder(all_season=True).all_player_averages()
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
    finder = statfinder.StatFinder(all_season=True)
    performances = statfinder.get_season_performances()
    accolades = finder.accolade_counts()
    return render(request, "stats/performances.html", {"performances": performances, "accolades": accolades})

# A class that returns the recent games for a player
def recent_season_games(request, id):
    season = Season.objects.filter(current_season=True).first()
    games = PlayerGameStats.objects.filter(Q(player_id=id) & Q(game__season=season)).order_by("-game__week")
    return render(request, "stats/recent_season_games.html", {"games": games})