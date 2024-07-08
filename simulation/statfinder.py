# Python improts

# Django imports
from django.db import models
from django.core.cache import cache

# Local imports
import simulation.config as config
from stats.models import Game, TeamGameStats, PlayerGameStats

current_week = config.CONFIG_SEASON["CURRENT_WEEK"]
current_season = config.CONFIG_SEASON["CURRENT_SEASON"]

class StatFinder:

    def __init__(self, week=current_week, season=current_season, fetch_all_season=False, fetch_all_time=False):
        if fetch_all_season:
            self.games = Game.objects.filter(season=season)
        elif fetch_all_time:
            self.games = Game.objects.all()
        else:
            self.games = Game.objects.filter(week=week, season=season)

    def player_averages(self, player, team=None):
        player_box_scores = PlayerGameStats.objects.filter(player=player)
        cache.set(key="player_averages", value=player_box_scores, timeout=3600)
        return player_box_scores.aggregate(
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
    
    def team_averages(self, team):
        team_box_scores = TeamGameStats.objects.filter(team=team)
        cache.set(key="team_averages", value=team_box_scores, timeout=3600)
        return team_box_scores.aggregate(
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
            models.Avg("time_of_possession"),
        )
    
    def player_totals(self, player, team=None):
        player_box_scores = PlayerGameStats.objects.filter(player=player)
        cache.set(key="player_totals", value=player_box_scores, timeout=3600)
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
        team_box_scores = TeamGameStats.objects.filter(team=team)
        cache.set(key="team_totals", value=team_box_scores, timeout=3600)
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
    