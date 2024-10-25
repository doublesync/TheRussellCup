# Python imports
import json

# Django imports
from django.views.decorators.http import require_GET
from django.http import HttpResponse
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import Q

# Local imports
import simulation.artificial as artificial
from players.models import Player
from teams.models import Team
from stats.models import Season, Game, PlayerGameStats, TeamGameStats, PlayerSeasonStats, TeamSeasonStats
import simulation.statfinder as statfinder

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
    season_list = sorted(Season.objects.all().values_list("season", flat=True), reverse=True)
    return render(request, "stats/player_averages.html", {"page_obj": season_stats, "stat_fields": stat_fields, "season_list": season_list})

# A function that returns the 'team_averages' page
def stats_home(request):
    finder = statfinder.StatFinder()
    standings = finder.league_standings()
    leaders = finder.league_leaders()
    season = Season.objects.filter(current_season=True).first()
    game_of_season = PlayerGameStats.objects.filter(game__season=season, team__surge=False).order_by("-game_score").first() # Not the best way to do this
    storylines = season.current_storylines
    recent_games = Game.objects.filter(season=season).order_by("-created")[:10]
    return render(request, "stats/stats_home.html", {"standings": standings, "storylines": storylines, "recent_games": recent_games, "leaders": leaders, "game_of_season": game_of_season})

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

# A function that allows a user to create a new game Entree
def create_game(request):
    context = {
        "players": Player.objects.all(),
        "teams": Team.objects.all(),
    }
    return render(request, "stats/create_game.html", context)

# A function that displays boxscore data from a specific game
def boxscore(request, id): 
    game = Game.objects.get(id=id)
    player_stats = PlayerGameStats.objects.filter(game=game)
    team_stats = TeamGameStats.objects.filter(game=game)
    return render(request, "stats/boxscore.html", {"game": game, "player_stats": player_stats, "team_stats": team_stats})

# A function that displays league averages for the season
def league_averages(request):
    finder = statfinder.StatFinder()
    league_averages = finder.league_averages() # Get league averages
    return render(request, "stats/league_averages.html", {"league_averages": league_averages})

# API Function for 'PlayerSeasonStats'
@require_GET
def league_stats_api(request):
    # Get the season parameter from the request
    season_param = request.GET.get("season")
    if season_param:
        season = Season.objects.filter(season=season_param).first()
    else:
        season = Season.objects.filter(current_season=True).first()
    if not season:
        return JsonResponse({"error": "Season not found"}, status=404)

    # Convert the queryset to a list of dictionaries
    team_stats = TeamSeasonStats.objects.filter(season=season)
    player_stats = PlayerSeasonStats.objects.filter(season=season)
    team_data = list(team_stats.values())
    player_data = list(player_stats.values(
        'player__first_name', 
        'player__last_name', 
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
        'average_turnover_percentage',
    ))
    # Return the data
    return JsonResponse({"teams": team_data, "players": player_data}, safe=False)