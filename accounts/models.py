from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Custom user model that extends the default Django user model.
    """

    can_pay_players = models.BooleanField(default=False)
    can_mark_upgrades = models.BooleanField(default=False)
    has_care_package = models.BooleanField(default=False)
    has_second_player_slot = models.BooleanField(default=False)

    def __str__(self):
        return self.username
