# Django imports
from django.db import models

# Local imports
import simulation.scripts.default as default
import simulation.scripts.animation as animation
import simulation.scripts.utility as utility

# fmt:off

# Custom field to disable validation on choice fields
class ChoiceFieldNoValidation(models.CharField):
    def validate(self):
        return

# Create your models here.
class Player(models.Model):
    
    # User defined fields
    first_name = models.CharField(max_length=16)
    last_name = models.CharField(max_length=16)
    position = models.CharField(
        max_length=2, choices=[(x, x) for x in default.position_choices]
    )
    number = models.IntegerField()
    country = models.CharField(max_length=64, choices=[(x, x) for x in default.country_choices])
    college = models.CharField(max_length=64, choices=[(x, x) for x in default.college_choices])
    # Randomly generated fields
    height = models.IntegerField(default=0)
    height_imperial = models.CharField(max_length=4, default="N/A")
    weight = models.IntegerField(default=0)
    wingspan = models.IntegerField(default=0)
    jumpshot = models.CharField(default="N/A", max_length=32)
    anomaly = models.BooleanField(default=False)
    # Server defined fields
    attributes = models.JSONField(default=default.default_attributes)
    badges = models.JSONField(default=default.default_badges)
    tendencies = models.JSONField(default=default.default_tendencies, null=True, blank=True)
    sim_rating = models.FloatField(default=0.00)
    # Foreign key fields
    user = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE, null=True, blank=True)
    team = models.ForeignKey("teams.Team", on_delete=models.CASCADE, null=True, blank=True)
    # Timestamp fields
    created = models.DateTimeField(auto_now_add=True)
    # Miscanellous fields
    retired = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        # Set the imperial height based on the height
        self.height_imperial = utility.imperial_height(self.height)
        # Set a random jumpshot if it is not set
        if self.jumpshot == "N/A":
            self.jumpshot = animation.jumpshot_roll(self.height)
        # Calculate the lateral quickness after potential upgrades
        self.attributes["Lateral Quickness"] = (
            self.attributes["Speed"] + self.attributes["Perimeter Defense"]
        ) // 2
        # Calculate the overall rating after potential upgrades
        self.sim_rating = round((sum(self.attributes.values()) / len(self.attributes)), 2)
        # Call the parent save method
        super(Player, self).save(*args, **kwargs)


# fmt:on
