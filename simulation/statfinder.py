# Python improts

# Django imports
from django.db import models
from django.core.cache import cache

# Local imports
import simulation.config as config
from stats.models import Game, TeamGameStats, PlayerGameStats

current_week = config.CONFIG_SEASON["CURRENT_WEEK"]
current_season = config.CONFIG_SEASON["CURRENT_SEASON"]


# Do the filter queries not work (?)
class StatFinder:

    def __init__(self, week=current_week, season=current_season, fetch_all_season=False, fetch_all_time=False):
        if fetch_all_season:
            self.games = Game.get_cached_queryset(filter_kwargs={"season": season})
        elif fetch_all_time:
            self.games = Game.get_cached_queryset()
        else:
            self.games = Game.get_cached_queryset(filter_kwargs={"week": week, "season": season})

    def safe_division(self, numerator, denominator):
        try:
            if denominator != 0:
                return round((numerator / denominator), 2)
            else:
                return 0
        except:
            return 0

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

    def player_averages(self, player, team=None):
        player_box_scores = PlayerGameStats.get_cached_queryset(filter_kwargs={"player": player})
        aggregates = player_box_scores.aggregate(
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
        )
        # Calculate shooting percentages
        fgm, fga = aggregates["field_goals_made__avg"], aggregates["field_goals_attempted__avg"]
        tpm, tpa = aggregates["three_pointers_made__avg"], aggregates["three_pointers_attempted__avg"]
        ftm, fta = aggregates["free_throws_made__avg"], aggregates["free_throws_attempted__avg"]
        aggregates["field_goal_percentage"] = self.safe_division(fgm, fga)
        aggregates["three_point_percentage"] = self.safe_division(tpm, tpa)
        aggregates["free_throw_percentage"] = self.safe_division(ftm, fta)
        aggregates["games"] = player_box_scores.count()
        # Round all aggregates
        for key in aggregates:
            if aggregates[key] and key != "games":
                aggregates[key] = round(aggregates[key], 2)
        # If team is provided, calculate team averages
        return aggregates
    
    def team_averages(self, team):
        team_box_scores = TeamGameStats.get_cached_queryset(filter_kwargs={"team": team})
        aggregates = team_box_scores.aggregate(
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
        aggregates["field_goal_percentage"] = self.safe_division(fgm, fga)
        aggregates["three_point_percentage"] = self.safe_division(tpm, tpa)
        aggregates["free_throw_percentage"] = self.safe_division(ftm, fta)
        aggregates["games"] = team_box_scores.count()
        # Round all aggregates
        for key in aggregates:
            if aggregates[key] and key != "games":
                aggregates[key] = round(aggregates[key], 2)
        # If team is provided, calculate team averages
        return aggregates
    
    def player_totals(self, player, team=None):
        player_box_scores = PlayerGameStats.get_cached_queryset(filter_kwargs={"player": player})
        return player_box_scores.aggregate(
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
        )
    
    def team_totals(self, team):
        team_box_scores = TeamGameStats.get_cached_queryset(filter_kwargs={"team": team})
        return team_box_scores.aggregate(
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