# Python imports

# Django imports
from django.core.cache import cache
from django.db import models
from django.db.models import Q

# Local imports
import simulation.config as config
from players.models import Player
from teams.models import Team
from stats.models import Season, Game, TeamGameStats, PlayerGameStats

# Set the current week and season
current_week = config.CONFIG_SEASON["CURRENT_WEEK"]
current_season = Season.objects.filter(current_season=True).first()

# A function to set all None values in a dictionary to 0
def none_to_zero(dictionary):
    for key in dictionary:
        if dictionary[key] is None:
            dictionary[key] = 0
    return dictionary

# A function to safely divide two numbers
def safe_division(numerator, denominator):
    try:
        if denominator != 0:
            return round((numerator / denominator), 2)
        else:
            return 0
    except:
        return 0

# A manager class to find statistics
class StatFinder:

    def __init__(self, season=current_season, specific_season=None, specific_week=None):

        # StatFinder Functions
        # - Get the games, player box scores, and team box scores
        # - Get player averages and totals
        # - Get team averages and totals
        # - Get league standings
        # - Get tiebreakers
        # - Get best and worst performances
        # - Get accolade counts
        # - Set game highs

        # StatFinder Usage
        # - By default, StatFinder will get the current seasons statistics
        # - If a specific season is provided, it will get the statistics for that season
        # - If a specific week is provided, it will get the statistics for that week
        # - If a specific season and week are provided, it will get the statistics for that season and week

        # Set the kwargs
        self.kwargs = {"season": season} # Kwargs for game models
        self.child_kwargs = {"game__season": season} # Child kwargs for playergamestats and teamgamestats models

        # Add to the kwargs if a specific season or week is provided
        if specific_season:
            self.kwargs["season"] = specific_season
            self.child_kwargs["game__season"] = specific_season
        if specific_week:
            self.kwargs["week"] = specific_week
            self.child_kwargs["game__week"] = specific_week

        # Get the games, player box scores, and team box scores
        self.games = Game.objects.filter(playoffgame__isnull=True, **self.kwargs)
        self.player_box_scores = PlayerGameStats.objects.filter(**self.child_kwargs)
        self.team_box_scores = TeamGameStats.objects.filter(**self.child_kwargs)

    def team_averages_totals(self, team):
        # Get all the players on the team
        player_list = team.player_set.all()
        # Get player averages and totals
        player_averages = {}
        player_totals = {}
        for player in player_list:
            player_averages[player] = self.player_averages(player)
            player_totals[player] = self.player_totals(player)
        # Get team averages and totals
        team_averages = self.team_averages(team)
        team_totals = self.team_totals(team)
        # Return all the data
        return {
            "player_averages": player_averages,
            "player_totals": player_totals,
            "team_averages": team_averages,
            "team_totals": team_totals
        }

    def all_player_averages(self):
        # Get all the players and get their averages
        player_averages = {}
        players = Player.objects.all()
        for player in players:
            player_averages[player] = self.player_averages(player)
        # Return all the player averages
        return player_averages

    def player_averages(self, player):
        box_scores = self.player_box_scores.filter(player=player)
        aggregates = box_scores.aggregate(
            # Basic stats
            models.Avg("minutes"),
            models.Avg("points"), 
            models.Avg("rebounds"), 
            models.Avg("assists"),
            models.Avg("steals"),
            models.Avg("blocks"),
            models.Avg("turnovers"),
            models.Avg("field_goals_made"),
            models.Avg("field_goals_attempted"),
            models.Avg("three_pointers_made"),
            models.Avg("three_pointers_attempted"),
            models.Avg("free_throws_made"),
            models.Avg("free_throws_attempted"),
            models.Avg("offensive_rebounds"),
            models.Avg("defensive_rebounds"),
            models.Avg("personal_fouls"),
            models.Avg("plus_minus"),
            models.Avg("points_responsible_for"),
            models.Avg("dunks"),
            # Advanced stats
            models.Avg("game_score"),
            models.Avg("effective_field_goal_percentage"),
            models.Avg("true_shooting_percentage"),
            models.Avg("turnover_percentage"),
        )
        # Calculate shooting percentages
        fgm, fga = aggregates["field_goals_made__avg"], aggregates["field_goals_attempted__avg"]
        tpm, tpa = aggregates["three_pointers_made__avg"], aggregates["three_pointers_attempted__avg"]
        ftm, fta = aggregates["free_throws_made__avg"], aggregates["free_throws_attempted__avg"]
        aggregates["field_goal_percentage"] = safe_division(fgm, fga)
        aggregates["three_point_percentage"] = safe_division(tpm, tpa)
        aggregates["free_throw_percentage"] = safe_division(ftm, fta)
        aggregates["games"] = box_scores.count()
        # Round all aggregates
        for key in aggregates:
            if aggregates[key] and key != "games":
                aggregates[key] = round(aggregates[key], 2)
        # Set None values to 0
        aggregates["full_name"] = f"{player.first_name} {player.last_name}"
        aggregates["position"] = player.position
        aggregates = none_to_zero(aggregates)
        # If team is provided, calculate team averages
        return aggregates
    
    def team_averages(self, team):
        # Get all the box scores for the team & get their averages
        box_scores = self.team_box_scores.filter(team=team)
        aggregates = box_scores.aggregate(
            models.Avg("field_goals_made"), 
            models.Avg("field_goals_attempted"),
            models.Avg("three_pointers_made"),
            models.Avg("three_pointers_attempted"),
            models.Avg("free_throws_made"),
            models.Avg("free_throws_attempted"),
            models.Avg("fast_break_points"),
            models.Avg("points_in_paint"),
            models.Avg("second_chance_points"),
            models.Avg("bench_points"),
            models.Avg("assists"),
            models.Avg("offensive_rebounds"),
            models.Avg("defensive_rebounds"),
            models.Avg("steals"),
            models.Avg("blocks"),
            models.Avg("turnovers"),
            models.Avg("points_off_turnovers"),
            models.Avg("personal_fouls"),
            models.Avg("dunks"),
            models.Avg("biggest_lead"),
        )
        # Calculate shooting percentages
        fgm, fga = aggregates["field_goals_made__avg"], aggregates["field_goals_attempted__avg"]
        tpm, tpa = aggregates["three_pointers_made__avg"], aggregates["three_pointers_attempted__avg"]
        ftm, fta = aggregates["free_throws_made__avg"], aggregates["free_throws_attempted__avg"]
        aggregates["field_goal_percentage"] = safe_division(fgm, fga)
        aggregates["three_point_percentage"] = safe_division(tpm, tpa)
        aggregates["free_throw_percentage"] = safe_division(ftm, fta)
        aggregates["games"] = box_scores.count()
        # Round all aggregates
        for key in aggregates:
            if aggregates[key] and key != "games":
                aggregates[key] = round(aggregates[key], 2)
        # Find some more standing statistics
        point_differentials = []
        for box_score in box_scores:
            standing_stats = box_score.get_point_differential()
            point_differentials.append(standing_stats["point_differential"])
        aggregates["point_differential"] = round(safe_division(sum(point_differentials), len(point_differentials)), 2)
        # Set None values to 0
        aggregates = none_to_zero(aggregates)
        # If team is provided, calculate team averages
        return aggregates
    
    def player_totals(self, player):
        # Get all the box scores for the player & get their totals
        box_scores = self.player_box_scores.filter(player=player)
        aggregates = box_scores.aggregate(
            # Basic stats
            models.Sum("minutes"),
            models.Sum("points"), 
            models.Sum("rebounds"), 
            models.Sum("assists"),
            models.Sum("steals"),
            models.Sum("blocks"),
            models.Sum("turnovers"),
            models.Sum("field_goals_made"),
            models.Sum("field_goals_attempted"),
            models.Sum("three_pointers_made"),
            models.Sum("three_pointers_attempted"),
            models.Sum("free_throws_made"),
            models.Sum("free_throws_attempted"),
            models.Sum("offensive_rebounds"),
            models.Sum("defensive_rebounds"),
            models.Sum("personal_fouls"),
            models.Sum("plus_minus"),
            models.Sum("points_responsible_for"),
            models.Sum("dunks"),
            # Advanced stats
            models.Sum("game_score"),
            models.Sum("effective_field_goal_percentage"),
            models.Sum("true_shooting_percentage"),
            models.Sum("turnover_percentage"),
        )
        # Set None values to 0
        aggregates["full_name"] = f"{player.first_name} {player.last_name}"
        aggregates = none_to_zero(aggregates)
        return aggregates
    
    def team_totals(self, team):
        # Get all the players on the team & get their totals
        box_scores = self.team_box_scores.filter(team=team)
        aggregates = box_scores.aggregate(
            models.Sum("field_goals_made"), 
            models.Sum("field_goals_attempted"),
            models.Sum("three_pointers_made"),
            models.Sum("three_pointers_attempted"),
            models.Sum("free_throws_made"),
            models.Sum("free_throws_attempted"),
            models.Sum("fast_break_points"),
            models.Sum("points_in_paint"),
            models.Sum("second_chance_points"),
            models.Sum("bench_points"),
            models.Sum("assists"),
            models.Sum("offensive_rebounds"),
            models.Sum("defensive_rebounds"),
            models.Sum("steals"),
            models.Sum("blocks"),
            models.Sum("turnovers"),
            models.Sum("points_off_turnovers"),
            models.Sum("personal_fouls"),
            models.Sum("dunks"),
            models.Sum("biggest_lead"),
            models.Sum("time_of_possession"),
        )
        # Add the games played, won, and lost
        aggregates["games"] = box_scores.count()
        aggregates["games_won"] = box_scores.filter(game__winner=team).count()
        aggregates["games_lost"] = (aggregates["games"] - aggregates["games_won"])
        # Find some more standing statistics
        point_differentials = []
        for box_score in box_scores:
            standing_stats = box_score.get_point_differential()
            point_differentials.append(standing_stats["point_differential"])
        aggregates["point_differential"] = sum(point_differentials)
        # Set None values to 0
        aggregates = none_to_zero(aggregates)
        return aggregates
    
    def tie_breakers(self, team):
        # Check for tiebreakers in the cache first
        if cache.get(f"tiebreakers_{team.id}"):
            return cache.get(f"tiebreakers_{team.id}")
        else:
            # Get the team's head-to-head record
            tallies = {}
            tiebreakers = []
            # Check each game the team has played against every other team to check if they have tiebreakers against every other team
            for game in self.team_box_scores.filter(team=team):
                opponent = game.game.away_team if game.game.home_team == team else game.game.home_team
                if opponent not in tallies:
                    tallies[opponent] = {
                        "games_won": 0,
                        "games_lost": 0,
                    }
                if game.game.winner == team:
                    tallies[opponent]["games_won"] += 1
                else:
                    tallies[opponent]["games_lost"] += 1
            # Check the tiebreakers in tallies
            for opponent in tallies:
                if tallies[opponent]["games_won"] > tallies[opponent]["games_lost"]:
                    tiebreakers.append(f"{opponent.city} {opponent.name}")
            # Set the tiebreakers in the cache
            cache.set(f"tiebreakers_{team.id}", tiebreakers, 60 * 60)
            # Return the tie breakers
            return tiebreakers

    def league_standings(self):
        # Get all the teams and get their totals
        teams = Team.objects.all()
        team_standings = {}
        for team in teams:
            team_standings[team.id] = {
                "team": team,
                "totals": self.team_totals(team)
            }
        # Sort the teams by wins
        # Let's set a secondary sorter using the "point_differential" key
        sorted_teams = {k: v for k, v in sorted(team_standings.items(), key=lambda item: (item[1]["totals"]["games_won"], item[1]["totals"]["point_differential"]), reverse=True)}
        # Add tiebreakers to the team standings
        for team_id in sorted_teams:
            team = sorted_teams[team_id]["team"]
            tiebreakers = self.tie_breakers(team)
            sorted_teams[team_id]["tiebreakers"] = tiebreakers
        # Return all the team standings
        return sorted_teams

    def best_performance(self):
        # Get the highest gamescore from the list of games
        box_scores_exist = self.player_box_scores.exists()
        if box_scores_exist:
            best_performance = self.player_box_scores.latest("game_score")
            # Return all the player performances
            return best_performance
        else:
            return None
    
    def worst_performance(self):
        # Get the lowest gamescore from the list of games
        box_scores_exist = self.player_box_scores.exists()
        if box_scores_exist:
            best_performance = self.player_box_scores.earliest("game_score")
            return best_performance
        else:
            return None

    def accolade_counts(self):
        # Let's initialize the accolade counts dictionary
        accolade_counts = {}
        # Each accolade in 'accolade_counts' should store the top three players who have achieved the accolade. The players should have a key of their name, and a value of the number of times they have achieved the accolade.
        accolade_counts["40+ Points"] = self.player_box_scores.filter(points__gte=40).values("player__first_name", "player__last_name").annotate(count=models.Count("player")).order_by("-count")[:3]
        accolade_counts["30+ Points"] = self.player_box_scores.filter(points__gte=30).values("player__first_name", "player__last_name").annotate(count=models.Count("player")).order_by("-count")[:3]
        accolade_counts["20+ Rebounds"] = self.player_box_scores.filter(rebounds__gte=20).values("player__first_name", "player__last_name").annotate(count=models.Count("player")).order_by("-count")[:3]
        accolade_counts["10+ Rebounds"] = self.player_box_scores.filter(rebounds__gte=10).values("player__first_name", "player__last_name").annotate(count=models.Count("player")).order_by("-count")[:3]
        accolade_counts["10+ Assists"] = self.player_box_scores.filter(assists__gte=10).values("player__first_name", "player__last_name").annotate(count=models.Count("player")).order_by("-count")[:3]
        accolade_counts["15+ Assists"] = self.player_box_scores.filter(assists__gte=15).values("player__first_name", "player__last_name").annotate(count=models.Count("player")).order_by("-count")[:3]
        accolade_counts["10+ Assists"] = self.player_box_scores.filter(assists__gte=10).values("player__first_name", "player__last_name").annotate(count=models.Count("player")).order_by("-count")[:3]
        accolade_counts["5+ Steals"] = self.player_box_scores.filter(steals__gte=5).values("player__first_name", "player__last_name").annotate(count=models.Count("player")).order_by("-count")[:3]
        accolade_counts["5+ Blocks"] = self.player_box_scores.filter(blocks__gte=5).values("player__first_name", "player__last_name").annotate(count=models.Count("player")).order_by("-count")[:3]
        # Check for triple doubles & double doubles
        accolade_counts["Triple Doubles"] = self.player_box_scores.filter(points__gte=10, rebounds__gte=10, assists__gte=10).values("player__first_name", "player__last_name").annotate(count=models.Count("player")).order_by("-count")[:3]
        accolade_counts["Double Doubles"] = self.player_box_scores.filter(models.Q(points__gte=10, rebounds__gte=10) | models.Q(points__gte=10, assists__gte=10) | models.Q(rebounds__gte=10, assists__gte=10)).values("player__first_name", "player__last_name").annotate(count=models.Count("player")).order_by("-count")[:3]
        # Return the accolade counts
        return accolade_counts

    def set_game_highs(self, season):

        highest_points = self.player_box_scores.latest("points")
        season.highest_points["game_id"] = highest_points.game.id
        season.highest_points["label"] = f"({highest_points.points}) {highest_points.player.first_name} {highest_points.player.last_name}"

        highest_rebounds = self.player_box_scores.latest("rebounds")
        season.highest_rebounds["game_id"] = highest_rebounds.game.id
        season.highest_rebounds["label"] = f"({highest_rebounds.rebounds}) {highest_rebounds.player.first_name} {highest_rebounds.player.last_name}"

        highest_assists = self.player_box_scores.latest("assists")
        season.highest_assists["game_id"] = highest_assists.game.id
        season.highest_assists["label"] = f"({highest_assists.assists}) {highest_assists.player.first_name} {highest_assists.player.last_name}"

        highest_steals = self.player_box_scores.latest("steals")
        season.highest_steals["game_id"] = highest_steals.game.id
        season.highest_steals["label"] = f"({highest_steals.steals}) {highest_steals.player.first_name} {highest_steals.player.last_name}"

        highest_blocks = self.player_box_scores.latest("blocks")
        season.highest_blocks["game_id"] = highest_blocks.game.id
        season.highest_blocks["label"] = f"({highest_blocks.blocks}) {highest_blocks.player.first_name} {highest_blocks.player.last_name}"

        highest_turnovers = self.player_box_scores.latest("turnovers")
        season.highest_turnovers["game_id"] = highest_turnovers.game.id
        season.highest_turnovers["label"] = f"({highest_turnovers.turnovers}) {highest_turnovers.player.first_name} {highest_turnovers.player.last_name}"

        highest_field_goals_made = self.player_box_scores.latest("field_goals_made")
        season.highest_field_goals_made["game_id"] = highest_field_goals_made.game.id
        season.highest_field_goals_made["label"] = f"({highest_field_goals_made.field_goals_made}) {highest_field_goals_made.player.first_name} {highest_field_goals_made.player.last_name}"

        highest_field_goals_attempted = self.player_box_scores.latest("field_goals_attempted")
        season.highest_field_goals_attempted["game_id"] = highest_field_goals_attempted.game.id
        season.highest_field_goals_attempted["label"] = f"({highest_field_goals_attempted.field_goals_attempted}) {highest_field_goals_attempted.player.first_name} {highest_field_goals_attempted.player.last_name}"

        highest_three_pointers_made = self.player_box_scores.latest("three_pointers_made")
        season.highest_three_pointers_made["game_id"] = highest_three_pointers_made.game.id
        season.highest_three_pointers_made["label"] = f"({highest_three_pointers_made.three_pointers_made}) {highest_three_pointers_made.player.first_name} {highest_three_pointers_made.player.last_name}"

        highest_three_pointers_attempted = self.player_box_scores.latest("three_pointers_attempted")
        season.highest_three_pointers_attempted["game_id"] = highest_three_pointers_attempted.game.id
        season.highest_three_pointers_attempted["label"] = f"({highest_three_pointers_attempted.three_pointers_attempted}) {highest_three_pointers_attempted.player.first_name} {highest_three_pointers_attempted.player.last_name}"

        highest_free_throws_made = self.player_box_scores.latest("free_throws_made")
        season.highest_free_throws_made["game_id"] = highest_free_throws_made.game.id
        season.highest_free_throws_made["label"] = f"({highest_free_throws_made.free_throws_made}) {highest_free_throws_made.player.first_name} {highest_free_throws_made.player.last_name}"

        highest_free_throws_attempted = self.player_box_scores.latest("free_throws_attempted")
        season.highest_free_throws_attempted["game_id"] = highest_free_throws_attempted.game.id
        season.highest_free_throws_attempted["label"] = f"({highest_free_throws_attempted.free_throws_attempted}) {highest_free_throws_attempted.player.first_name} {highest_free_throws_attempted.player.last_name}"

        highest_offensive_rebounds = self.player_box_scores.latest("offensive_rebounds")
        season.highest_offensive_rebounds["game_id"] = highest_offensive_rebounds.game.id
        season.highest_offensive_rebounds["label"] = f"({highest_offensive_rebounds.offensive_rebounds}) {highest_offensive_rebounds.player.first_name} {highest_offensive_rebounds.player.last_name}"

        highest_defensive_rebounds = self.player_box_scores.latest("defensive_rebounds")
        season.highest_defensive_rebounds["game_id"] = highest_defensive_rebounds.game.id
        season.highest_defensive_rebounds["label"] = f"({highest_defensive_rebounds.defensive_rebounds}) {highest_defensive_rebounds.player.first_name} {highest_defensive_rebounds.player.last_name}"

        highest_personal_fouls = self.player_box_scores.latest("personal_fouls")
        season.highest_personal_fouls["game_id"] = highest_personal_fouls.game.id
        season.highest_personal_fouls["label"] = f"({highest_personal_fouls.personal_fouls}) {highest_personal_fouls.player.first_name} {highest_personal_fouls.player.last_name}"

        highest_plus_minus = self.player_box_scores.latest("plus_minus")
        season.highest_plus_minus["game_id"] = highest_plus_minus.game.id
        season.highest_plus_minus["label"] = f"({highest_plus_minus.plus_minus}) {highest_plus_minus.player.first_name} {highest_plus_minus.player.last_name}"

        highest_points_responsible_for = self.player_box_scores.latest("points_responsible_for")
        season.highest_points_responsible_for["game_id"] = highest_points_responsible_for.game.id
        season.highest_points_responsible_for["label"] = f"({highest_points_responsible_for.points_responsible_for}) {highest_points_responsible_for.player.first_name} {highest_points_responsible_for.player.last_name}"

        highest_dunks = self.player_box_scores.latest("dunks")
        season.highest_dunks["game_id"] = highest_dunks.game.id
        season.highest_dunks["label"] = f"({highest_dunks.dunks}) {highest_dunks.player.first_name} {highest_dunks.player.last_name}"

        highest_game_score = self.player_box_scores.latest("game_score")
        season.highest_game_score["game_id"] = highest_game_score.game.id
        season.highest_game_score["label"] = f"({highest_game_score.game_score}) {highest_game_score.player.first_name} {highest_game_score.player.last_name}"

        highest_effective_field_goal_percentage = self.player_box_scores.latest("effective_field_goal_percentage")
        season.highest_effective_field_goal_percentage["game_id"] = highest_effective_field_goal_percentage.game.id
        season.highest_effective_field_goal_percentage["label"] = f"({highest_effective_field_goal_percentage.effective_field_goal_percentage}) {highest_effective_field_goal_percentage.player.first_name} {highest_effective_field_goal_percentage.player.last_name}"

        highest_true_shooting_percentage = self.player_box_scores.latest("true_shooting_percentage")
        season.highest_true_shooting_percentage["game_id"] = highest_true_shooting_percentage.game.id
        season.highest_true_shooting_percentage["label"] = f"({highest_true_shooting_percentage.true_shooting_percentage}) {highest_true_shooting_percentage.player.first_name} {highest_true_shooting_percentage.player.last_name}"

        highest_turnover_percentage = self.player_box_scores.latest("turnover_percentage")
        season.highest_turnover_percentage["game_id"] = highest_turnover_percentage.game.id
        season.highest_turnover_percentage["label"] = f"({highest_turnover_percentage.turnover_percentage}) {highest_turnover_percentage.player.first_name} {highest_turnover_percentage.player.last_name}"

        season.save()

def get_season_performances():
    performances = {}
    current_week = config.CONFIG_SEASON["CURRENT_WEEK"]
    # Get the best and worst performances for each week
    for week in range(1, current_week + 1):
        # Get the best for the iterated week of the current season (defaults to current season)
        finder = StatFinder(specific_week=week)
        performances[week] = {
            "week": week,
            "best": finder.best_performance(),
            "worst": finder.worst_performance()
        }
    # Return all the performances
    return performances