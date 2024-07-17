# Python imports
import hashlib
import datetime

# Django imports
from django.db import models
from django.core.cache import cache
from django.utils.functional import cached_property
from django.utils import timezone
from django.contrib import messages

# Local imports
import simulation.scripts.default as default
from players.models import Player
from teams.models import Team


# Create your managers here.
class GameManager(models.Manager):
    def queryset_from_cache(self, filterdict):
        cachekey = 'GameCache' + hashlib.md5(str(filterdict).encode()).hexdigest()
        res = cache.get(cachekey)
        if res:
            return res  # Return only the queryset from cache
        else:
            res = Game.objects.filter(**filterdict)
            cache.set(cachekey, res, 300)  # Five minutes
            return res

class TeamGameStatsManager(models.Manager):
    def queryset_from_cache(self, filterdict):
        cachekey = 'TeamGameStatsCache' + hashlib.md5(str(filterdict).encode()).hexdigest()
        res = cache.get(cachekey)
        if res:
            return res  # Return only the queryset from cache
        else:
            res = TeamGameStats.objects.filter(**filterdict)
            cache.set(cachekey, res, 300)  # Five minutes
            return res
        
class PlayerGameStatsManager(models.Manager):
    def queryset_from_cache(self, filterdict):
        cachekey = 'PlayerGameStatsCache' + hashlib.md5(str(filterdict).encode()).hexdigest()
        res = cache.get(cachekey)
        if res:
            return res  # Return only the queryset from cache
        else:
            res = PlayerGameStats.objects.filter(**filterdict)
            cache.set(cachekey, res, 300)  # Five minutes
            return res

# Create your models here.
class Season(models.Model):
    
    # Defined fields
    season = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"S{self.season}"

class Game(models.Model):

    # Managers
    objects = GameManager()

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
        # Automatically set the winner of the game
        self.winner = self.get_winner()
        # Prevent non-staff users from saving games that are older than 24 hours
        if not self.created or self.created > timezone.now() - datetime.timedelta(days=1):
            super(Game, self).save(*args, **kwargs)
            
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

    def save(self, *args, **kwargs):
        # Prevent non-staff users from saving games that are older than 24 hours
        if not self.created or self.created > timezone.now() - datetime.timedelta(days=1):
            super(TeamGameStats, self).save(*args, **kwargs)

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
        self.game_score = round((self.points + (0.4 * self.field_goals_made) - (0.7 * self.field_goals_attempted) - (0.4 * (self.free_throws_attempted - self.free_throws_made)) + (0.7 * self.offensive_rebounds) + (0.3 * self.defensive_rebounds) + self.steals + (0.7 * self.assists) + (0.7 * self.blocks) - (0.4 * self.personal_fouls) - self.turnovers), 2)
        self.effective_field_goal_percentage = round(((self.field_goals_made + (0.5 * self.three_pointers_made)) / self.field_goals_attempted), 2)
        self.true_shooting_percentage = round((self.points / (2 * (self.field_goals_attempted + (0.44 * self.free_throws_attempted)))), 2)
        self.turnover_percentage = round((self.turnovers / (self.field_goals_attempted + (0.44 * self.free_throws_attempted) + self.turnovers)), 2)

    def save(self, *args, **kwargs):
        # Automatically calculate the points & defensive rebounds scored by the player
        self.points = (self.field_goals_made * 2) + (self.three_pointers_made) + (self.free_throws_made)
        self.defensive_rebounds = (self.rebounds - self.offensive_rebounds)
        # Prevent non-staff users from saving games that are older than 24 hours
        if not self.created or self.created > timezone.now() - datetime.timedelta(days=1):
            # Set the advanced stats
            self.set_advanced_stats()
            super(PlayerGameStats, self).save(*args, **kwargs)
