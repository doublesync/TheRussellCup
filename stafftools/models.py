# Django imports
from django.db import models

# Local imports
from accounts.models import CustomUser
from players.models import Player

# Create your models here.
class PaymentRequest(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    sp_amount = models.IntegerField(default=0, help_text="Amount in SP")
    xp_amount = models.IntegerField(default=0, help_text="Amount in XP")
    reason = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)