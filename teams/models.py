# Python imports
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
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.city} {self.name}"

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