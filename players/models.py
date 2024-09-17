# Python imports

# Django imports
from django.db import models

# Local imports
from simulation.frivolity import SimulationRating
import simulation.config as config
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
    svg_image = models.TextField(default="", blank=True, null=True)
    sp_spent = models.IntegerField(default=0)
    xp_spent = models.IntegerField(default=0)
    # Randomly generated fields
    height = models.IntegerField(default=0)
    height_imperial = models.CharField(max_length=4, default="N/A")
    weight = models.IntegerField(default=0)
    wingspan = models.IntegerField(default=0)
    # Randomly generated jumpshot fields & anomaly field
    jumpshot = models.CharField(default="N/A", max_length=32, null=True, blank=True)
    jumpshot_release_1 = models.CharField(default="N/A", max_length=32, null=True, blank=True)
    jumpshot_release_2 = models.CharField(default="N/A", max_length=32, null=True, blank=True)
    jumpshot_blending = models.IntegerField(default=0, null=True, blank=True)
    jumpshot_timing = models.CharField(default="N/A", max_length=32, null=True, blank=True)
    jumpshot_free_throw = models.CharField(default="N/A", max_length=32, null=True, blank=True)
    anomaly = models.BooleanField(default=False)
    # Server defined fields
    attributes = models.JSONField(default=default.default_attributes)
    badges = models.JSONField(default=default.default_badges)
    tendencies = models.JSONField(default=default.default_tendencies, null=True, blank=True)
    coach_suggestion_attributes = models.JSONField(default=dict, null=True, blank=True)
    coach_suggestion_badges = models.JSONField(default=dict, null=True, blank=True)
    coach_suggestion_tendencies = models.JSONField(default=dict, null=True, blank=True)
    sim_rating = models.FloatField(default=0.00)
    # Foreign key fields
    user = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE, null=True, blank=True)
    team = models.ForeignKey("teams.Team", on_delete=models.CASCADE, null=True, blank=True)
    contract = models.ForeignKey("logs.ContractLog", on_delete=models.CASCADE, null=True, blank=True, related_name="contract")
    # Timestamp fields
    created = models.DateTimeField(auto_now_add=True)
    # Miscanellous fields
    retired = models.BooleanField(default=False)
    on_roster = models.BooleanField(default=False)
    modifications = models.JSONField(default=default.default_modifications, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        # Set the imperial height based on the height
        self.height_imperial = utility.imperial_height(self.height)
        # Set a random jumpshot if it is not set
        if not self.jumpshot or self.jumpshot == "N/A": animation.generate_jumpshot(self)
        # Calculate the overall rating after potential upgrades
        rating_manager = SimulationRating(self)
        self.sim_rating = rating_manager.get_rating()
        # Call the parent save method
        super(Player, self).save(*args, **kwargs)

class Modification(models.Model):

    # User defined fields
    item = models.CharField(max_length=64)
    xp_price = models.IntegerField(default=0)
    xp_price_with_discount = models.IntegerField(default=0, help_text="This is automatically calculated.")
    multi_buy = models.BooleanField(default=False)
    # Timestamp fields
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item} - {self.xp_price} XP"
    
    def save(self, *args, **kwargs):
        # Calculate the price with the discount
        self.xp_price_with_discount = self.xp_price - (self.xp_price * config.CONFIG_USER["CARE_PACKAGE_MOD_DISCOUNT"])
        # Call the parent save method
        super(Modification, self).save(*args, **kwargs)

# fmt:on
