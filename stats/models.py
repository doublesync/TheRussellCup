# Python imports
import hashlib
import datetime

# Django imports
from django.db import models
from django.utils import timezone

# Local imports
from stats.managers import GameManager, TeamGameStatsManager, PlayerGameStatsManager
from players.models import Player
import simulation.scripts.default as default
from teams.models import Team

# This is so messy...
def default_game_highs():
    return {
        "game_id": 0,
        "label": "N/A",
    }

# Create your models here.
class Season(models.Model):
    
    # Defined fields
    current_season = models.BooleanField(default=True)
    season = models.IntegerField()
    highest_points = models.JSONField(default=default_game_highs, null=True, blank=True)
    highest_rebounds = models.JSONField(default=default_game_highs, null=True, blank=True)
    highest_assists = models.JSONField(default=default_game_highs, null=True, blank=True)
    highest_steals = models.JSONField(default=default_game_highs, null=True, blank=True)
    highest_blocks = models.JSONField(default=default_game_highs, null=True, blank=True)
    highest_turnovers = models.JSONField(default=default_game_highs, null=True, blank=True)
    highest_field_goals_made = models.JSONField(default=default_game_highs, null=True, blank=True)
    highest_field_goals_attempted = models.JSONField(default=default_game_highs, null=True, blank=True)
    highest_three_pointers_made = models.JSONField(default=default_game_highs, null=True, blank=True)
    highest_three_pointers_attempted = models.JSONField(default=default_game_highs, null=True, blank=True)
    highest_free_throws_made = models.JSONField(default=default_game_highs, null=True, blank=True)
    highest_free_throws_attempted = models.JSONField(default=default_game_highs, null=True, blank=True)
    highest_offensive_rebounds = models.JSONField(default=default_game_highs, null=True, blank=True)
    highest_personal_fouls = models.JSONField(default=default_game_highs, null=True, blank=True)
    highest_plus_minus = models.JSONField(default=default_game_highs, null=True, blank=True)
    highest_points_responsible_for = models.JSONField(default=default_game_highs, null=True, blank=True)
    highest_dunks = models.JSONField(default=default_game_highs, null=True, blank=True)
    highest_defensive_rebounds = models.JSONField(default=default_game_highs, null=True, blank=True)
    highest_game_score = models.JSONField(default=default_game_highs, null=True, blank=True)
    highest_effective_field_goal_percentage = models.JSONField(default=default_game_highs, null=True, blank=True)
    highest_true_shooting_percentage = models.JSONField(default=default_game_highs, null=True, blank=True)
    highest_turnover_percentage = models.JSONField(default=default_game_highs, null=True, blank=True)
    
    # OpenAI fields
    current_storylines = models.TextField(default="There are no current storylines", blank=True, null=True)

    def __str__(self):
        return f"S{self.season}"

class Playoff(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    quarterfinals = models.ForeignKey("PlayoffRound", on_delete=models.CASCADE, related_name="quarterfinals", blank=True, null=True)
    semifinals = models.ForeignKey("PlayoffRound", on_delete=models.CASCADE, related_name="semifinals", blank=True, null=True)
    finals = models.ForeignKey("PlayoffRound", on_delete=models.CASCADE, related_name="finals", blank=True, null=True)

    def __str__(self):
        return f"Playoffs | {self.season}"

class PlayoffRound(models.Model):
    playoff = models.ForeignKey(Playoff, on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=((choice, choice) for choice in default.playoff_round_choices))
    wins_to_advance = models.IntegerField(default=5)

    def __str__(self):
        return f"{self.type} | {self.playoff}"

class PlayoffSeries(models.Model):
    round = models.ForeignKey(PlayoffRound, on_delete=models.CASCADE)
    team_a = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team_a")
    team_b = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team_b")
    team_a_seed = models.IntegerField()
    team_b_seed = models.IntegerField()
    winner = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="series_winner", blank=True, null=True)

    def __str__(self):
        return f"{self.round} | {self.team_a.name} vs {self.team_b.name}"
    
    class Meta:
        verbose_name_plural = "Playoff series"

class Game(models.Model):

    # Managers
    objects = GameManager()

    # Defined fields
    surge_game = models.BooleanField(default=False)
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
        loser = self.home_team if self.winner == self.away_team else self.away_team
        return f"{self.season}-W{self.week} | {self.winner.name} beat {loser.name} ({self.home_team_score}-{self.away_team_score})"
        
    def save(self, *args, **kwargs):
        # Automatically set the winner of the game
        self.winner = self.get_winner()
        # Prevent non-staff users from saving games that are older than 10 days
        if not self.created or self.created > timezone.now() - datetime.timedelta(days=10):
            super(Game, self).save(*args, **kwargs)

class PlayoffGame(Game):
    
    # Defined fields
    series = models.ForeignKey(PlayoffSeries, on_delete=models.CASCADE)
    game_number = models.IntegerField()

    def __str__(self):
        loser = self.home_team if self.winner == self.away_team else self.away_team
        return f"{self.series.round} | {self.series.team_a.name} vs {self.series.team_b.name} | Game {self.game_number} | {self.winner.name} beat {loser.name} ({self.home_team_score}-{self.away_team_score})"

class TeamGameStats(models.Model):

    # Managers
    objects = TeamGameStatsManager()

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
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.team} | Game {self.game}"

    def get_point_differential(self):
        total_points = self.game.home_team_score if self.team == self.game.home_team else self.game.away_team_score
        points_against = self.game.away_team_score if self.team == self.game.home_team else self.game.home_team_score
        point_differential = total_points - points_against
        return {
            "point_differential": point_differential,
        }


    def save(self, *args, **kwargs):
        # Prevent non-staff users from saving games that are older than 10 days
        if not self.created or self.created > timezone.now() - datetime.timedelta(days=10):
            super(TeamGameStats, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Team game stats"

class PlayerGameStats(models.Model):

    # Managers
    objects = PlayerGameStatsManager()

    # Defined fields
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
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
    defensive_rebounds = models.IntegerField(default=0, help_text="Automatically calculated field")
    created = models.DateTimeField(auto_now_add=True)

    # Advanced stat fields
    game_score = models.FloatField(default=0.0, help_text="Automatically calculated field")
    effective_field_goal_percentage = models.FloatField(default=0.0, help_text="Automatically calculated field")
    true_shooting_percentage = models.FloatField(default=0.0, help_text="Automatically calculated field")
    turnover_percentage = models.FloatField(default=0.0, help_text="Automatically calculated field")

    class Meta:
        get_latest_by = "game_score"

    def __str__(self):
        return f"{self.player} Game {self.game} Stats"
    
    def set_team(self):
        if self.player.team:
            self.team = self.player.team
            self.save()

    def set_advanced_stats(self):
        # Automatically calculate the game score of the player
        self.game_score = round((self.points + (0.4 * self.field_goals_made) - (0.7 * self.field_goals_attempted) - (0.4 * (self.free_throws_attempted - self.free_throws_made)) + (0.7 * self.offensive_rebounds) + (0.3 * self.defensive_rebounds) + self.steals + (0.7 * self.assists) + (0.7 * self.blocks) - (0.4 * self.personal_fouls) - self.turnovers), 2)
        # Prevents floating point division by zero
        try:
            self.effective_field_goal_percentage = round(((self.field_goals_made + (0.5 * self.three_pointers_made)) / self.field_goals_attempted), 2)
        except ZeroDivisionError:
            self.effective_field_goal_percentage = 0.0
        # Prevents floating point division by zero
        try:
            self.true_shooting_percentage = round((self.points / (2 * (self.field_goals_attempted + (0.44 * self.free_throws_attempted)))), 2)
        except ZeroDivisionError:
            self.true_shooting_percentage = 0.0
        # Prevents floating point division by zero
        try:
            self.turnover_percentage = round((self.turnovers / (self.field_goals_attempted + (0.44 * self.free_throws_attempted) + self.turnovers)), 2)
        except ZeroDivisionError:
            self.turnover_percentage = 0.0

    def save(self, *args, **kwargs):
        # Automatically calculate the points & defensive rebounds scored by the player
        self.points = (self.field_goals_made * 2) + (self.three_pointers_made) + (self.free_throws_made)
        self.defensive_rebounds = (self.rebounds - self.offensive_rebounds)
        self.set_advanced_stats()
        # Prevent non-staff users from saving games that are older than 10 days
        if not self.created or self.created > timezone.now() - datetime.timedelta(days=10):
            super(PlayerGameStats, self).save(*args, **kwargs)


    class Meta:
        verbose_name_plural = "Player game stats"