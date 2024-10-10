# Django imports
from django.db import models

# Local imports
from players.models import Player

# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    rookies_allowed = models.BooleanField(default=False)
    free_agents_allowed = models.BooleanField(default=False)
    active_players_allowed = models.BooleanField(default=False)
    use_spent_limit = models.BooleanField(default=False)
    spent_limit = models.IntegerField(default=0)
    max_entries = models.IntegerField(default=0)

    def __str__(self):
        return self.title

# Yes, it's spelled "Entree" and not "Entry" due to the fact that I can't spell
class Entree(models.Model): 
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.player} - {self.event}"
    
    class Meta:
        verbose_name = "Entry"
        verbose_name_plural = "Entries"