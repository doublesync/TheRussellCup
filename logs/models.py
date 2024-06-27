# Django imports
from django.db import models

# Local imports
import simulation.config as config

# A model to store the upgrade logs
class UpgradeLog(models.Model):
    player = models.ForeignKey("players.Player", on_delete=models.CASCADE)
    total_sp = models.IntegerField()
    total_xp = models.IntegerField()
    upgrades = models.JSONField()
    week = models.IntegerField(default=config.CONFIG_SEASON["CURRENT_WEEK"])
    season = models.IntegerField(default=config.CONFIG_SEASON["CURRENT_SEASON"])
    created = models.DateTimeField(auto_now_add=True)

# A model to store the payment logs
class PaymentLog(models.Model):
    staff = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE)
    player = models.ForeignKey("players.Player", on_delete=models.CASCADE)
    payment = models.IntegerField()
    reason = models.CharField(max_length=255)
    type = models.CharField(max_length=2, choices=(("SP", "SP"), ("XP", "XP")))
    week = models.IntegerField(default=config.CONFIG_SEASON["CURRENT_WEEK"])
    season = models.IntegerField(default=config.CONFIG_SEASON["CURRENT_SEASON"])
    created = models.DateTimeField(auto_now_add=True)
