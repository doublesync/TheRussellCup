# Django imports
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import ForeignKey

# Local imports


# We need to add a field tot he User model to store the user's profile picture
class CustomUser(AbstractUser):
    sp = models.IntegerField(default=0)
    xp = models.IntegerField(default=0)
    can_pay_players = models.BooleanField(default=False)
    can_mark_upgrades = models.BooleanField(default=False)
    has_care_package = models.BooleanField(default=False)
    has_second_player_slot = models.BooleanField(default=False)

    def __str__(self):
        return self.username
