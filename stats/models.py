# Python imports


# Django imports
from typing import Iterable
from django.db import models


# Local imports
import simulation.scripts.default as default
from players.models import Player
from teams.models import Team


# Create your models here.

class Season(models.Model):
    
    # Defined fields
    season = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"S{self.season}"

class Game(models.Model):

    # Defined fields
    surge_game = models.BooleanField(default=False)
    game_type = models.CharField(max_length=100, choices=[(game_type, game_type) for game_type in default.game_type_choices])
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    week = models.IntegerField()
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="home_team")
    home_team_score = models.IntegerField()
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="away_team")
    away_team_score = models.IntegerField()
    winner = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="winner", blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def get_winner(self):
        if self.home_team_score > self.away_team_score:
            return self.home_team
        elif self.away_team_score > self.home_team_score:
            return self.away_team

    def __str__(self):
        return f"{self.season}, W{self.week} | {self.home_team} vs. {self.away_team} |"
        
    def save(self, *args, **kwargs):
        self.winner = self.get_winner()
        super(Game, self).save(*args, **kwargs)

class TeamGameStats(models.Model):

    # Defined fields
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    field_goals_made = models.IntegerField()
    field_goals_attempted = models.IntegerField()
    three_pointers_made = models.IntegerField()
    three_pointers_attempted = models.IntegerField()
    free_throws_made = models.IntegerField()
    free_throws_attempted = models.IntegerField()
    fast_break_points = models.IntegerField()
    points_in_paint = models.IntegerField()
    second_chance_points = models.IntegerField()
    bench_points = models.IntegerField(default=0)
    assists = models.IntegerField()
    offensive_rebounds = models.IntegerField()
    defensive_rebounds = models.IntegerField()
    steals = models.IntegerField()
    blocks = models.IntegerField()
    turnovers = models.IntegerField()
    points_off_turnovers = models.IntegerField()
    personal_fouls = models.IntegerField()
    dunks = models.IntegerField()
    biggest_lead = models.IntegerField()
    time_of_possession = models.DurationField()

    def __str__(self):
        return f"{self.team} Game Stats"

class PlayerGameStats(models.Model):

    # Defined fields
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    minutes = models.IntegerField()
    points = models.IntegerField(help_text="Automatically calculated field")
    rebounds = models.IntegerField()
    assists = models.IntegerField()
    steals = models.IntegerField()
    blocks = models.IntegerField()
    turnovers = models.IntegerField()
    field_goals_made = models.IntegerField()
    field_goals_attempted = models.IntegerField()
    three_pointers_made = models.IntegerField()
    three_pointers_attempted = models.IntegerField()
    free_throws_made = models.IntegerField()
    free_throws_attempted = models.IntegerField()
    offensive_rebounds = models.IntegerField()
    personal_fouls = models.IntegerField()
    plus_minus = models.IntegerField()
    points_responsible_for = models.IntegerField()
    dunks = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    defensive_rebounds = models.IntegerField(default=0, help_text="Automatically calculated field")

    def __str__(self):
        return f"{self.player} Game {self.game} Stats"
    
    def save(self, *args, **kwargs):
        self.points = (self.field_goals_made * 2) + (self.three_pointers_made) + (self.free_throws_made)
        self.defensive_rebounds = (self.rebounds - self.offensive_rebounds)
        super(PlayerGameStats, self).save(*args, **kwargs)
