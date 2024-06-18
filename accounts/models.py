# Django imports
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import ForeignKey

# Local imports


# We need to add a field tot he User model to store the user's profile picture, sp, and xp
class CustomUser(AbstractUser):
    avatar = models.URLField(
        default="https://www.gravatar.com/avatar/205e460b479e2e5b48aec07710c08d50"
    )
    sp = models.IntegerField(default=0)
    xp = models.IntegerField(default=0)

    def __str__(self):
        return self.username
