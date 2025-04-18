from django.db import models

from players.models import Player


class Event(models.Model):
    """
    Model representing an event in the league.
    """

    title = models.CharField(max_length=100)
    description = models.TextField()
    rookies_allowed = models.BooleanField(default=False)
    free_agents_allowed = models.BooleanField(default=False)
    active_players_allowed = models.BooleanField(default=False)
    use_spent_limit = models.BooleanField(default=False)
    spent_limit = models.IntegerField(default=0)
    max_entries = models.IntegerField(default=0)

    def __str__(self):
        """
        String representation of the Event model.
        """

        return str(self.title)


class Entree(models.Model):
    """
    Model representing an entry in the league.
    """

    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.player} - {self.event}"

    class Meta:
        """
        Meta options for the Entree model.
        """

        verbose_name = "Entry"
        verbose_name_plural = "Entries"
