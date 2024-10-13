# Python imports

# Django imports
from django.core.cache import cache
from django.db import models
from django.db.models import Q

# Local imports
import simulation.config as config
from players.models import Player
from teams.models import Team
from stats.models import Season, Game, TeamGameStats, PlayerGameStats, PlayerSeasonStats, TeamSeasonStats

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

    def __init__(self, season=current_season, specific_season=None, specific_week=None, only_playoffs=False, surge=False):

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
        self.kwargs = {"season": season, "surge_game": surge} # Kwargs for game models
        self.child_kwargs = {"game__season": season, "team__surge": surge} # Child kwargs for playergamestats and teamgamestats models

        # Add to the kwargs if a specific season or week is provided
        if specific_season:
            self.kwargs["season"] = specific_season
            self.child_kwargs["game__season"] = specific_season
        if specific_week:
            self.kwargs["week"] = specific_week
            self.child_kwargs["game__week"] = specific_week

        # Add playoff game filter if the season is only for playoffs
        self.kwargs["playoffgame__isnull"] = False if only_playoffs else True
        self.child_kwargs["game__playoffgame__isnull"] = False if only_playoffs else True

        # Get the games, player box scores, and team box scores
        self.games = Game.objects.filter(**self.kwargs)
        self.player_box_scores = PlayerGameStats.objects.filter(**self.child_kwargs)
        self.team_box_scores = TeamGameStats.objects.filter(**self.child_kwargs)

    # Returns team & player averages and totals for a specific team
    def team_player_stats(self, team):
        # Get all the players on the team
        player_list = team.player_set.all()
        # Get player averages and totals
        player_season_stats = {}
        for player in player_list:
            player_season_stats[player] = self.player_stats(player)
        # Return all the data
        return {
            "player_season_stats": player_season_stats,
            "team_season_stats": self.team_stats(team)
        }

    # Returns 'PlayerSeasonStats' objects for every eligible player in the season
    def all_player_stats(self, query=None, order_by=None):
        player_list = PlayerSeasonStats.objects.filter(season=self.kwargs["season"])
        if query:
            player_list = player_list.filter(query)
            if order_by:
                player_list = player_list.order_by(order_by)
        return player_list

    # Returns 'PlayerSeasonStats' object for a specific player in the season
    def player_stats(self, player):
        # Get the player season stats for the player
        player_season = self.kwargs["season"]
        player_season_stats = PlayerSeasonStats.objects.filter(player=player, season=player_season).first()
        # If the player season stats are not found, get the latest player season stats
        if not player_season_stats:
            player_season_stats = PlayerSeasonStats.objects.filter(player=player).first()
        # Return the player season stats
        return player_season_stats

    # Returns 'TeamSeasonStats' object for a specific team in the season
    def team_stats(self, team):
        # Get the team season stats for the team
        team_season = self.kwargs["season"]
        team_season_stats = TeamSeasonStats.objects.filter(team=team, season=team_season).first()
        # If the team season stats are not found, get the latest team season stats
        if not team_season_stats:
            team_season_stats = TeamSeasonStats.objects.filter(team=team).first()
        # Return the team season stats
        return team_season_stats

    # Returns specific teams a team has tiebreakers against
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

    # Returns the league standings for the season
    def league_standings(self):
        # Get all the teams and get their totals
        include_surge = self.kwargs["surge_game"]
        teams = Team.objects.filter(surge=include_surge)
        team_standings = {}
        for team in teams:
            season_stats = self.team_stats(team)
            if season_stats:
                team_standings[team.id] = {
                    "team": team,
                    "season_stats": season_stats
                }
        # Sort the teams by wins
        # Let's set a secondary sorter using the "point_differential" key
        sorted_teams = {k: v for k, v in sorted(team_standings.items(), key=lambda item: (item[1]["season_stats"].wins, item[1]["season_stats"].point_differential), reverse=True)}
        # Add tiebreakers to the team standings
        for team_id in sorted_teams:
            team = sorted_teams[team_id]["team"]
            tiebreakers = self.tie_breakers(team)
            sorted_teams[team_id]["tiebreakers"] = tiebreakers
        # Return all the team standings
        return sorted_teams

    # Returns the best performance from configured game list
    def best_performance(self):
        # Get the highest gamescore from the list of games
        box_scores_exist = self.player_box_scores.exists()
        if box_scores_exist:
            best_performance = self.player_box_scores.latest("game_score")
            # Return all the player performances
            return best_performance
        else:
            return None
    
    # Returns the worst performance from configured game list
    def worst_performance(self):
        # Get the lowest gamescore from the list of games
        box_scores_exist = self.player_box_scores.exists()
        if box_scores_exist:
            best_performance = self.player_box_scores.earliest("game_score")
            return best_performance
        else:
            return None

    # Returns accolade counts for the season
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

    # Set the game highs for the season
    def set_game_highs(self):

        season = self.kwargs["season"]

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


# Returns the season performances for the current season
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
