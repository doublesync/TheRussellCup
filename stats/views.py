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
from stats.models import Season, Game, PlayerGameStats, TeamGameStats, PlayerSeasonStats
import simulation.statfinder as statfinder
from django_table_sort.table import TableSort

# Create your views here.
    
# A function that returns the 'player_averages' page
def player_averages(request):
    stat_fields = [
        'games_played',
        'minutes',
        'points',
        'rebounds',
        'assists',
        'steals',
        'blocks',
        'turnovers',
        'field_goals_made',
        'field_goals_attempted',
        'three_pointers_made',
        'three_pointers_attempted',
        'free_throws_made',
        'free_throws_attempted',
        'offensive_rebounds',
        'personal_fouls',
        'plus_minus',
        'points_responsible_for',
        'dunks',
        'defensive_rebounds',
        'game_score',
        'effective_field_goal_percentage',
        'true_shooting_percentage',
        'turnover_percentage',
        'average_minutes',
        'average_points',
        'average_rebounds',
        'average_assists',
        'average_steals',
        'average_blocks',
        'average_turnovers',
        'average_field_goals_made',
        'average_field_goals_attempted',
        'average_field_goal_percentage',
        'average_three_pointers_made',
        'average_three_pointers_attempted',
        'average_three_point_percentage',
        'average_free_throws_made',
        'average_free_throws_attempted',
        'average_free_throw_percentage',
        'average_offensive_rebounds',
        'average_personal_fouls',
        'average_plus_minus',
        'average_points_responsible_for',
        'average_dunks',
        'average_defensive_rebounds',
        'average_game_score',
        'average_effective_field_goal_percentage',
        'average_true_shooting_percentage',
        'average_turnover_percentage'
    ]
    finder = statfinder.StatFinder()
    season_stats = finder.all_player_stats()
    season_list = Season.objects.all().values_list("season", flat=True)
    return render(request, "stats/player_averages.html", {"page_obj": season_stats, "stat_fields": stat_fields, "season_list": season_list})

# A function that returns the 'team_averages' page
def stats_home(request):
    finder = statfinder.StatFinder()
    standings = finder.league_standings()
    season = Season.objects.filter(current_season=True).first()
    storylines = season.current_storylines
    return render(request, "stats/stats_home.html", {"standings": standings, "storylines": storylines})

# A function that sorts the players by a given stat
def sort_by_stat(request, stat):
    if request.method == "POST":
        # Get the averages for each player
        players = statfinder.StatFinder().all_player_stats()
        # Sort by the stat & make a dictionary of players
        order_type = request.POST.get("order-type")
        reverse_order = False if order_type == "asc" else True
        # Sort queryset by stat
        sorted_players = players.order_by(stat) if reverse_order else players.order_by(f"-{stat}")
        # Render to string
        fragment_html = render_to_string("stats/fragments/list_fragment.html", {"players": sorted_players})
        return HttpResponse(fragment_html)

# A function that returns the records page
def records(request):
    season = Season.objects.filter(current_season=True).first()
    return render(request, "stats/records.html", {"season": season})

# A function that returns the performances page
def performances(request):
    finder = statfinder.StatFinder()
    performances = statfinder.get_season_performances()
    accolades = finder.accolade_counts()
    return render(request, "stats/performances.html", {"performances": performances, "accolades": accolades})

# A function that returns the recent games for a player
def recent_season_games(request, id):
    season = Season.objects.filter(current_season=True).first()
    games = PlayerGameStats.objects.filter(Q(player_id=id) & Q(game__season=season)).order_by("-game__week")
    return render(request, "stats/recent_season_games.html", {"games": games})