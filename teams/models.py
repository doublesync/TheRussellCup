# Python imports

# Django imports
from django.db import models

# Local imports
from players.models import Player
from accounts.models import CustomUser

# Create your models here.
class Team(models.Model):

    # Defined fields
    manager = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    city = models.CharField(max_length=32)
    color = models.CharField(max_length=10, default="#434648")
    surge = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.city} {self.name}"

class TeamLogs(models.Model):

    # Defined fields (positions)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    # Defined fields (positions, playtypes, focus, & sliders)
    playbook = models.CharField(max_length=32, default="Team Playbook 1")
    offensive_focus = models.CharField(max_length=32, default="No Preference")
    offensive_tempo = models.CharField(max_length=32, default="No Preference")
    offensive_rebounding = models.CharField(max_length=32, default="No Preference")
    defensive_focus = models.CharField(max_length=32, default="No Preference")
    defensive_aggression = models.CharField(max_length=32, default="No Preference")
    defensive_rebounding = models.CharField(max_length=32, default="No Preference")
    run_plays = models.IntegerField(default=50)
    zone_usage = models.IntegerField(default=50)

    # Defined fields (position lineups, play initiators, playtypes, & touches)
    lineup = models.JSONField(default=dict)
    initiators = models.JSONField(default=dict)
    playtypes = models.JSONField(default=dict)
    touches = models.JSONField(default=dict)


class Draft(models.Model):

    # Defined fields
    season = models.IntegerField(unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Draft for Season {self.season}"
    
class DraftPick(models.Model):

    # Defined fields
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    draft = models.ForeignKey(Draft, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    round = models.IntegerField()
    pick = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.team} Round {self.round} Pick {self.pick} Player {self.player}"
    
class DraftOrder(models.Model):

    # Defined fields
    draft = models.ForeignKey(Draft, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    order = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.team} Order {self.order}"