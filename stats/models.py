# Python imports


# Django imports
from typing import Iterable
from django.db import models


# Local imports
from players.models import Player
from teams.models import Team


# Create your models here.
class Game(models.Model):

    # Defined fields
    winner = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="winner", blank=True, null=True)
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="home_team")
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="away_team")
    home_team_score = models.IntegerField()
    away_team_score = models.IntegerField()
    season = models.IntegerField()
    week = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def get_winner(self):
        if self.home_team_score > self.away_team_score:
            return self.home_team
        elif self.away_team_score > self.home_team_score:
            return self.away_team

    def __str__(self):
        return f"{self.home_team} vs. {self.away_team} | {self.home_team_score} - {self.away_team_score}"
        
    def save(self, *args, **kwargs):
        self.winner = self.get_winner()
        super(Game, self).save(*args, **kwargs)


class TeamGameStats(models.Model):

    # Defined fields
    points = models.IntegerField()
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
    points = models.IntegerField()
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
    defensive_rebounds = models.IntegerField(default=0)
    personal_fouls = models.IntegerField()
    plus_minus = models.IntegerField()
    points_responsible_for = models.IntegerField()
    dunks = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.player} Game {self.game} Stats"
    
    def save(self, *args, **kwargs):
        self.points = (self.field_goals_made * 2) + (self.three_pointers_made) + (self.free_throws_made)
        self.defensive_rebounds = (self.rebounds - self.offensive_rebounds)
        super(PlayerGameStats, self).save(*args, **kwargs)