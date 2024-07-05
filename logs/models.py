# Django imports
from django.db import models

# Local imports
import simulation.config as config
from players.models import Player, Modification

# A model to store the upgrade logs
class UpgradeLog(models.Model):
    player = models.ForeignKey("players.Player", on_delete=models.CASCADE)
    total_sp = models.IntegerField()
    total_xp = models.IntegerField()
    upgrades = models.JSONField()
    week = models.IntegerField(default=config.CONFIG_SEASON["CURRENT_WEEK"])
    season = models.IntegerField(default=config.CONFIG_SEASON["CURRENT_SEASON"])
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

# A model to store the payment logs
class PaymentLog(models.Model):
    staff = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE)
    player = models.ForeignKey("players.Player", on_delete=models.CASCADE)
    payment = models.IntegerField()
    reason = models.CharField(max_length=255)
    type = models.CharField(max_length=2)
    week = models.IntegerField(default=config.CONFIG_SEASON["CURRENT_WEEK"])
    season = models.IntegerField(default=config.CONFIG_SEASON["CURRENT_SEASON"])
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.staff.username} paid {self.player.user.username} ${self.payment} {self.type} for {self.reason}"
    
# A model to store the contract logs
class ContractLog(models.Model):
    player = models.ForeignKey("players.Player", on_delete=models.CASCADE)
    season = models.IntegerField()
    length = models.IntegerField()
    option = models.CharField(max_length=32, default="None")
    current_year_payment = models.IntegerField()
    subsequent_year_payment = models.IntegerField(default=0)
    biennium_year_payment = models.IntegerField(default=0)
    no_trade_clause = models.BooleanField(default=False)
    no_release_clause = models.BooleanField(default=False)
    incentives = models.CharField(max_length=255)
    weeks_paid = models.JSONField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"S{self.season} {self.player}"