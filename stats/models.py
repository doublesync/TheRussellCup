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

    @cached_property
    def cached_data(self):
        cache_key = f'game_{self.id}'
        game = cache.get(cache_key)
        if game is None:
            game = self
            cache.set(cache_key, game, timeout=900)
        return game

    @classmethod
    def get_cached_queryset(cls, filter_kwargs=None, cache_key=None, timeout=60*15):
        if filter_kwargs is None:
            filter_kwargs = {}

        if cache_key is None:
            cache_key = f"games_{hash(frozenset(filter_kwargs.items()))}"

        pks = cache.get(cache_key)
        if pks is None:
            queryset = cls.objects.filter(**filter_kwargs)
            pks = list(queryset.values_list('pk', flat=True))
            cache.set(cache_key, pks, timeout)

        # Reconstruct the queryset from the primary keys
        queryset = cls.objects.filter(pk__in=pks)

        return queryset
        
    def __str__(self):
        return f"{self.season}, W{self.week} | {self.home_team} vs. {self.away_team} |"
        
    def save(self, *args, **kwargs):
        # Automatically set the winner of the game
        self.winner = self.get_winner()
        # Prevent non-staff users from saving games that are older than 24 hours
        if self.created > timezone.now() - datetime.timedelta(days=1):
            super(PlayerGameStats, self).save(*args, **kwargs)
            
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
    created = models.DateTimeField(auto_now_add=True)

    @cached_property
    def cached_data(self):
        cache_key = f'teamgamestat_{self.id}'
        game_stat = cache.get(cache_key)
        if game_stat is None:
            game_stat = self
            cache.set(cache_key, game_stat, timeout=900)  # Cache for 15 minutes
        return game_stat

    @classmethod
    def get_cached_queryset(cls, filter_kwargs=None, cache_key=None, timeout=60*15):
        if filter_kwargs is None:
            filter_kwargs = {}

        if cache_key is None:
            cache_key = f"teamgamestats_{hash(frozenset(filter_kwargs.items()))}"

        pks = cache.get(cache_key)
        if pks is None:
            queryset = cls.objects.filter(**filter_kwargs)
            pks = list(queryset.values_list('pk', flat=True))
            cache.set(cache_key, pks, timeout)

        # Reconstruct the queryset from the primary keys
        queryset = cls.objects.filter(pk__in=pks)

        return queryset

    def __str__(self):
        return f"{self.team} Game Stats"
    
    def save(self, *args, **kwargs):
        # Prevent non-staff users from saving games that are older than 24 hours
        if self.created > timezone.now() - datetime.timedelta(days=1):
            super(PlayerGameStats, self).save(*args, **kwargs)

class PlayerGameStats(models.Model):

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

    @cached_property
    def cached_data(self):
        cache_key = f'playergamestat_{self.id}'
        game_stat = cache.get(cache_key)
        if game_stat is None:
            game_stat = self
            cache.set(cache_key, game_stat, timeout=900)  # Cache for 15 minutes
        return game_stat
    
    @classmethod
    def get_cached_queryset(cls, filter_kwargs=None, cache_key=None, timeout=60*15):
        if filter_kwargs is None:
            filter_kwargs = {}

        if cache_key is None:
            cache_key = f"playergamestats_{hash(frozenset(filter_kwargs.items()))}"

        pks = cache.get(cache_key)
        if pks is None:
            queryset = cls.objects.filter(**filter_kwargs)
            pks = list(queryset.values_list('pk', flat=True))
            cache.set(cache_key, pks, timeout)

        # Reconstruct the queryset from the primary keys
        queryset = cls.objects.filter(pk__in=pks)

        return queryset

    def __str__(self):
        return f"{self.player} Game {self.game} Stats"
    
    def set_team(self):
        if self.player.team:
            self.team = self.player.team
            self.save()

    def save(self, *args, **kwargs):
        # Automatically calculate the points & defensive rebounds scored by the player
        self.points = (self.field_goals_made * 2) + (self.three_pointers_made) + (self.free_throws_made)
        self.defensive_rebounds = (self.rebounds - self.offensive_rebounds)
        # Prevent non-staff users from saving games that are older than 24 hours
        if self.created > timezone.now() - datetime.timedelta(days=1):
            super(PlayerGameStats, self).save(*args, **kwargs)
