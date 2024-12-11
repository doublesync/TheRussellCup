# Python imports
import json

# Django imports
from django.views.decorators.http import require_GET
from django.http import HttpResponse
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render
from django.shortcuts import redirect
from django.db.models import Q
from django.urls import reverse

# Local imports
import simulation.config as config
import simulation.statfinder as statfinder
from players.models import Player
from teams.models import Team
from stats.models import Season, Game, PlayerGameStats, TeamGameStats, PlayerSeasonStats, TeamSeasonStats
from stats.forms import GameForm, PlayerGameStatsForm

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
    if not request.user.is_staff:
        return redirect("stats_home")
    context = {
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

# A function that fetches the roster for a team
def htmx_fetch_roster(request):

    # Get home and away team IDs
    home_team = request.GET.get("home_team")
    away_team = request.GET.get("away_team")
    # Check if both teams exist
    if not home_team or not away_team or home_team == away_team:
        return HttpResponse(
            f"""
            <p class="text-center text-lg font-semibold alert alert-secondary">
                Please select two different teams
            </p>
            """
        )
    # Fetch the team & players
    home_team = Team.objects.get(pk=home_team)
    away_team = Team.objects.get(pk=away_team)
    all_players = Player.objects.all() # inefficient; saving for later
    home_players = all_players.filter(team=home_team).values('id', 'first_name', 'last_name').distinct()
    away_players = all_players.filter(team=away_team).values('id', 'first_name', 'last_name').distinct()
    # Render the roster template
    roster_html = render_to_string(
        "stats/fragments/players_table.html", 
        {
            "home_team": home_team,
            "away_team": away_team,
            "home_players": home_players,
            "away_players": away_players
        }
    )
    return HttpResponse(roster_html)

# A function that creates a game based on the user's form
def htmx_confirm_game(request):
    
    if not request.user.is_staff:
        return redirect("stats_home")

    # Get the form data
    game_week = request.POST.get("game_week")
    surge_game = request.POST.get("surge_game")
    playoff_game = request.POST.get("playoff_game")
    home_team = request.POST.get("home_team")
    away_team = request.POST.get("away_team")
    home_team_points = request.POST.get("home_team_points")
    away_team_points = request.POST.get("away_team_points")

    # Validate the form variables
    # Surge game & playoff game will be an empty string (false) if not toggled
    if not game_week or not home_team or not away_team or not home_team_points or not away_team_points:
        return HttpResponse("<span class='text-danger'>Please fill out all fields</span>")

    # Print all of the player stats, they go <stat_name>-<player_id>
    player_stats = {}
    tracked_game_fields = config.CONFIG_STATS["TRACKED_GAME_FIELDS"]
    for key, value in request.POST.items():
        try:
            stat_name, player_id = key.split("-")
            if stat_name in tracked_game_fields:
                if "-" in key:
                    if player_id not in player_stats:
                        player_stats[player_id] = {}
                    player_stats[player_id][stat_name] = value
        except ValueError:
            continue

    # Validate the teams here
    home_team_exists = Team.objects.filter(pk=home_team).exists()
    away_team_exists = Team.objects.filter(pk=away_team).exists()
    if not home_team_exists or not away_team_exists:
        return HttpResponse("<span class='text-danger'>One or more teams do not exist</span>")
    # Get the team objects
    home_team = Team.objects.get(pk=home_team)
    away_team = Team.objects.get(pk=away_team)

    # Validate the form data
    game_validator = statfinder.GameValidator(home_team_points, away_team_points, player_stats)
    result, errors = game_validator.start()
    if not result:
        error_html = ""
        for error in errors:
            error_html += f"<span class='text-danger'>{error[1]}</span><br>"
        return HttpResponse(error_html)
    
    # Create the game
    game = Game.objects.create(
        surge_game=bool(surge_game),
        season=Season.objects.filter(current_season=True).first(),
        week=int(game_week),
        home_team=home_team,
        home_team_score=int(home_team_points),
        away_team=away_team,
        away_team_score=int(away_team_points)
    )
    teams_to_save = [home_team, away_team]

    # Create team game stats
    for team in teams_to_save:
        # Generate totals for stats from the player stats
        team_totals = {}
        for player_id, stats in player_stats.items():
            for key, value in stats.items():
                # Check if the stat is a player-only stat
                if key in ["plus_minus", "minutes", "points_responsible_for"]:
                    continue
                # Get the real key without the "-player_id" suffix
                real_key = key
                if "-" in key: 
                    real_key, player_id = key.split("-")
                # Check if the player is on the team
                if real_key in team_totals:
                    team_totals[real_key] += int(value)
                else:
                    team_totals[real_key] = int(value)
        print(json.dumps(team_totals, indent=4))
        # Create the team game stats
        TeamGameStats.objects.create(
            game=game,
            team=team,
            points=game.home_team_score if team == home_team else game.away_team_score,
            **team_totals # Unpack the team totals dictionary
        )

    # Save each team's season stats
    for team in teams_to_save:
        season_stats_exist = TeamSeasonStats.objects.filter(season=game.season, team=team).exists()
        if season_stats_exist:
            TeamSeasonStats.objects.get(season=game.season, team=team).save()
        else:
            TeamSeasonStats.objects.create(season=game.season, team=team).save()

    # Convert player_stats to a dictionary of ints
    for player_id, stats in player_stats.items():
        for key, value in stats.items():
            player_stats[player_id][key] = int(value)

    # Create the player stats
    for player_id, stats in player_stats.items():
        player = Player.objects.get(pk=player_id)
        # Create the player game stats
        PlayerGameStats.objects.create(
            game=game,
            player=player,
            team=player.team,
            **stats # Unpack the stats dictionary
        )
        # Update the player's season stats
        season_stats_exist = PlayerSeasonStats.objects.filter(season=game.season, player=player).exists()
        if season_stats_exist:
            PlayerSeasonStats.objects.get(season=game.season, player=player).save()
        else:
            PlayerSeasonStats.objects.create(season=game.season, player=player).save()

    # Return a response
    boxscore_url = reverse("boxscore", kwargs={"id": game.id})
    headers = {
        "HX-Redirect": boxscore_url
    }
    return HttpResponse("<span class='text-success'>Game successfully created</span>", headers=headers)