# Python imports
import hashlib
import datetime

# Django imports
from django.db import models
from django.utils import timezone

# Local imports
import simulation.config as config
import simulation.scripts.default as default
import simulation.webhook as webhook
from stats.managers import GameManager, TeamGameStatsManager, PlayerGameStatsManager
from players.models import Player
from teams.models import Team

# A function to safely divide two numbers
def safe_division(numerator, denominator):
    try:
        if denominator != 0:
            return round((numerator / denominator), 2)
        else:
            return 0
    except:
        return 0

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
        bypass = kwargs.pop("bypass", False)
        if bypass or not self.created or self.created > timezone.now() - datetime.timedelta(days=10):
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
    points = models.IntegerField(default=0, help_text="Automatically calculated field")
    rebounds = models.IntegerField(default=0, help_text="Automatically calculated field")
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
    point_differential = models.IntegerField(default=0)
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
        bypass = kwargs.pop("bypass", False)
        if bypass or not self.created or self.created > timezone.now() - datetime.timedelta(days=10):
            # Calculate points, point differential, & rebounds
            self.points = (self.field_goals_made * 2) + (self.three_pointers_made) + self.free_throws_made
            self.point_differential = self.get_point_differential()["point_differential"]
            self.rebounds = (self.defensive_rebounds + self.offensive_rebounds)
            # Save the season stats model (or create it if it doesn't exist)
            season_stats, _ = TeamSeasonStats.objects.get_or_create(season=self.game.season, team=self.team)
            season_stats.save()
            # Save the model
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
        bypass = kwargs.pop("bypass", False)
        if bypass or not self.created or self.created > timezone.now() - datetime.timedelta(days=10):
            # Save the season stats model (or create it if it doesn't exist)
            season_stats, created = PlayerSeasonStats.objects.get_or_create(season=self.game.season, player=self.player)
            season_stats.save()
            # Save the model
            super(PlayerGameStats, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Player game stats"

class PlayerSeasonStats(models.Model):

    # Defined fields
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

    # Basic stats
    games_played = models.IntegerField(default=0)
    minutes = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    rebounds = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)
    steals = models.IntegerField(default=0)
    blocks = models.IntegerField(default=0)
    turnovers = models.IntegerField(default=0)
    field_goals_made = models.IntegerField(default=0)
    field_goals_attempted = models.IntegerField(default=0)
    three_pointers_made = models.IntegerField(default=0)
    three_pointers_attempted = models.IntegerField(default=0)
    free_throws_made = models.IntegerField(default=0)
    free_throws_attempted = models.IntegerField(default=0)
    offensive_rebounds = models.IntegerField(default=0)
    personal_fouls = models.IntegerField(default=0)
    plus_minus = models.IntegerField(default=0)
    points_responsible_for = models.IntegerField(default=0)
    dunks = models.IntegerField(default=0)
    defensive_rebounds = models.IntegerField(default=0)
    game_score = models.FloatField(default=0.0)
    effective_field_goal_percentage = models.FloatField(default=0.0)
    true_shooting_percentage = models.FloatField(default=0.0)
    turnover_percentage = models.FloatField(default=0.0)

    # Average stats
    average_minutes = models.FloatField(default=0.0)
    average_points = models.FloatField(default=0.0)
    average_rebounds = models.FloatField(default=0.0)
    average_assists = models.FloatField(default=0.0)
    average_steals = models.FloatField(default=0.0)
    average_blocks = models.FloatField(default=0.0)
    average_turnovers = models.FloatField(default=0.0)
    average_field_goals_made = models.FloatField(default=0.0)
    average_field_goals_attempted = models.FloatField(default=0.0)
    average_field_goal_percentage = models.FloatField(default=0.0)
    average_three_pointers_made = models.FloatField(default=0.0)
    average_three_pointers_attempted = models.FloatField(default=0.0)
    average_three_point_percentage = models.FloatField(default=0.0)
    average_free_throws_made = models.FloatField(default=0.0)
    average_free_throws_attempted = models.FloatField(default=0.0)
    average_free_throw_percentage = models.FloatField(default=0.0)
    average_offensive_rebounds = models.FloatField(default=0.0)
    average_personal_fouls = models.FloatField(default=0.0)
    average_plus_minus = models.FloatField(default=0.0)
    average_points_responsible_for = models.FloatField(default=0.0)
    average_dunks = models.FloatField(default=0.0)
    average_defensive_rebounds = models.FloatField(default=0.0)
    average_game_score = models.FloatField(default=0.0)
    average_effective_field_goal_percentage = models.FloatField(default=0.0)
    average_true_shooting_percentage = models.FloatField(default=0.0)
    average_turnover_percentage = models.FloatField(default=0.0)

    # Game high stats
    game_high_points = models.IntegerField(default=0)
    game_high_rebounds = models.IntegerField(default=0)
    game_high_assists = models.IntegerField(default=0)
    game_high_steals = models.IntegerField(default=0)
    game_high_blocks = models.IntegerField(default=0)
    game_high_turnovers = models.IntegerField(default=0)
    game_high_field_goals_made = models.IntegerField(default=0)
    game_high_field_goals_attempted = models.IntegerField(default=0)
    game_high_three_pointers_made = models.IntegerField(default=0)
    game_high_three_pointers_attempted = models.IntegerField(default=0)
    game_high_free_throws_made = models.IntegerField(default=0)
    game_high_free_throws_attempted = models.IntegerField(default=0)
    game_high_offensive_rebounds = models.IntegerField(default=0)
    game_high_personal_fouls = models.IntegerField(default=0)
    game_high_plus_minus = models.IntegerField(default=0)
    game_high_points_responsible_for = models.IntegerField(default=0)
    game_high_dunks = models.IntegerField(default=0)
    game_high_defensive_rebounds = models.IntegerField(default=0)
    game_high_game_score = models.FloatField(default=0.0)
    game_high_effective_field_goal_percentage = models.FloatField(default=0.0)
    game_high_true_shooting_percentage = models.FloatField(default=0.0)
    game_high_turnover_percentage = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.player} | {self.season}"
        
    def save(self, *args, **kwargs):

# Make a list of fields to get the sum of

        # Get the sum of the fields in 'aggregate_fields'
        # Manually set the games played field
        # Set the sum of the fields in 'aggregate_fields' to the model
        # Calculate the average of the fields in 'aggregate_fields' based on the fields above
        # Set field goal percentages
        aggregate_fields = config.CONFIG_STATS["TRACKED_TOTALS_FIELDS"]
        aggregates = self.player.playergamestats_set.filter(game__season=self.season).aggregate(
            **{f"{field}__sum": models.Sum(field) for field in aggregate_fields}
        )
        for field in aggregate_fields:
            setattr(self, field, aggregates[f"{field}__sum"]) # Setting each total 
        self.games_played = self.player.playergamestats_set.filter(game__season=self.season).count() # Setting games played
        for field in aggregate_fields:
            total = getattr(self, field)
            setattr(self, f"average_{field}", round(total / self.games_played, 2)) # Setting each average
        if self.average_field_goals_attempted > 0:
            self.average_field_goal_percentage = round(self.average_field_goals_made / self.average_field_goals_attempted, 2)
        if self.average_three_pointers_attempted > 0:
            self.average_three_point_percentage = round(self.average_three_pointers_made / self.average_three_pointers_attempted, 2)
        if self.average_free_throws_attempted > 0:
            self.average_free_throw_percentage = round(self.average_free_throws_made / self.average_free_throws_attempted, 2)
        
        # Calculate game highs
        game_high_fields = config.CONFIG_STATS["TRACKED_GAME_HIGH_FIELDS"]
        for field in game_high_fields:
            game_high = self.player.playergamestats_set.filter(game__season=self.season).order_by(f"-{field}").first()
            game_high_value = getattr(game_high, field)
            setattr(self, f"game_high_{field}", game_high_value)
    
        # Save the model
        super(PlayerSeasonStats, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Player season stats"

class TeamSeasonStats(models.Model):

    # Defined fields
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    # Basic stats
    games_played = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    rebounds = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)
    steals = models.IntegerField(default=0)
    blocks = models.IntegerField(default=0)
    turnovers = models.IntegerField(default=0)
    field_goals_made = models.IntegerField(default=0)
    field_goals_attempted = models.IntegerField(default=0)
    three_pointers_made = models.IntegerField(default=0)
    three_pointers_attempted = models.IntegerField(default=0)
    free_throws_made = models.IntegerField(default=0)
    free_throws_attempted = models.IntegerField(default=0)
    defensive_rebounds = models.IntegerField(default=0)
    offensive_rebounds = models.IntegerField(default=0)
    personal_fouls = models.IntegerField(default=0)
    points_off_turnovers = models.IntegerField(default=0)
    points_in_paint = models.IntegerField(default=0)
    second_chance_points = models.IntegerField(default=0)
    dunks = models.IntegerField(default=0)
    biggest_lead = models.IntegerField(default=0)
    point_differential = models.IntegerField(default=0)

    # Average stats
    average_points = models.FloatField(default=0.0)
    average_rebounds = models.FloatField(default=0.0)
    average_assists = models.FloatField(default=0.0)
    average_steals = models.FloatField(default=0.0)
    average_blocks = models.FloatField(default=0.0)
    average_turnovers = models.FloatField(default=0.0)
    average_field_goals_made = models.FloatField(default=0.0)
    average_field_goals_attempted = models.FloatField(default=0.0)
    average_field_goal_percentage = models.FloatField(default=0.0)
    average_three_pointers_made = models.FloatField(default=0.0)
    average_three_pointers_attempted = models.FloatField(default=0.0)
    average_three_point_percentage = models.FloatField(default=0.0)
    average_free_throws_made = models.FloatField(default=0.0)
    average_free_throws_attempted = models.FloatField(default=0.0)
    average_free_throw_percentage = models.FloatField(default=0.0)
    average_defensive_rebounds = models.FloatField(default=0.0)
    average_offensive_rebounds = models.FloatField(default=0.0)
    average_personal_fouls = models.FloatField(default=0.0)
    average_points_off_turnovers = models.FloatField(default=0.0)
    average_points_in_paint = models.FloatField(default=0.0)
    average_second_chance_points = models.FloatField(default=0.0)
    average_dunks = models.FloatField(default=0.0)
    average_biggest_lead = models.FloatField(default=0.0)
    average_point_differential = models.FloatField(default=0.0)

    # Game high stats
    game_high_points = models.IntegerField(default=0)
    game_high_rebounds = models.IntegerField(default=0)
    game_high_assists = models.IntegerField(default=0)
    game_high_steals = models.IntegerField(default=0)
    game_high_blocks = models.IntegerField(default=0)
    game_high_turnovers = models.IntegerField(default=0)
    game_high_field_goals_made = models.IntegerField(default=0)
    game_high_field_goals_attempted = models.IntegerField(default=0)
    game_high_three_pointers_made = models.IntegerField(default=0)
    game_high_three_pointers_attempted = models.IntegerField(default=0)
    game_high_free_throws_made = models.IntegerField(default=0)
    game_high_free_throws_attempted = models.IntegerField(default=0)
    game_high_defensive_rebounds = models.IntegerField(default=0)
    game_high_offensive_rebounds = models.IntegerField(default=0)
    game_high_personal_fouls = models.IntegerField(default=0)
    game_high_points_off_turnovers = models.IntegerField(default=0)
    game_high_points_in_paint = models.IntegerField(default=0)
    game_high_second_chance_points = models.IntegerField(default=0)
    game_high_dunks = models.IntegerField(default=0)
    game_high_biggest_lead = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.team} | {self.season}"

    def save(self, *args, **kwargs):

        # Make a list of fields to get the sum of
        aggregate_fields = [
            "points", "rebounds", "assists", "steals", "blocks", "turnovers",
            "field_goals_made", "field_goals_attempted", "three_pointers_made", "three_pointers_attempted",
            "free_throws_made", "free_throws_attempted", "defensive_rebounds", "offensive_rebounds", "personal_fouls", 
            "points_off_turnovers", "points_in_paint", "second_chance_points", "dunks", "biggest_lead", "point_differential"
        ]
        # Get the sum of the fields in 'aggregate_fields'
        aggregates = self.team.teamgamestats_set.filter(game__season=self.season).aggregate(
            **{f"{field}__sum": models.Sum(field) for field in aggregate_fields}
        )
        # Set the sum of the fields in 'aggregate_fields' to the model
        for field in aggregate_fields:
            if aggregates[f"{field}__sum"] is None:
                setattr(self, field, 0)
            else:
                setattr(self, field, aggregates[f"{field}__sum"])
        # Calculate the average of the fields in 'aggregate_fields' based on the fields above
        for field in aggregate_fields:
            total = getattr(self, field) or 0
            setattr(self, f"average_{field}", round(safe_division(total, self.games_played), 2))
        # Set field goal percentages
        if self.average_field_goals_attempted > 0:
            self.average_field_goal_percentage = round(self.average_field_goals_made / self.average_field_goals_attempted, 2)
        if self.average_three_pointers_attempted > 0:
            self.average_three_point_percentage = round(self.average_three_pointers_made / self.average_three_pointers_attempted, 2)
        if self.average_free_throws_attempted > 0:
            self.average_free_throw_percentage = round(self.average_free_throws_made / self.average_free_throws_attempted, 2)
        # Calculate game highs
        game_high_fields = [
            "points", "rebounds", "assists", "steals", "blocks", "turnovers",
            "field_goals_made", "field_goals_attempted", "three_pointers_made", "three_pointers_attempted", "free_throws_made",
            "free_throws_attempted", "defensive_rebounds", "offensive_rebounds", "personal_fouls", "points_off_turnovers", "points_in_paint", 
            "second_chance_points", "dunks", "biggest_lead"
        ]
        for field in game_high_fields:
            game_high = self.team.teamgamestats_set.filter(game__season=self.season).order_by(f"-{field}").first()
            game_high_value = getattr(game_high, field) if game_high else 0 # Important to check if game_high is None
            setattr(self, f"game_high_{field}", game_high_value)
        # Calculate the number of wins and losses, points, total rebounds
        self.games_played = self.team.teamgamestats_set.filter(game__season=self.season).count()
        self.wins = self.team.teamgamestats_set.filter(game__season=self.season, game__winner=self.team).count()
        self.losses = self.games_played - self.wins

        # Save the model
        super(TeamSeasonStats, self).save(*args, **kwargs) 

        # Send a webhook to the Discord server
        webhook.send_webhook(url="stat_updates", title="Team Season Stats Updated", body=f"{self.team.city} {self.team.name}'s season stats have been updated for the {self.season} season.")

    class Meta:
        verbose_name_plural = "Team season stats"
