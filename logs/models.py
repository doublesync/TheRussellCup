from django.db import models

import simulation.config as config


class UpgradeLog(models.Model):
    """
    A model to store the upgrade logs for players.
    """

    player = models.ForeignKey("players.Player", on_delete=models.CASCADE)
    total_sp = models.IntegerField()
    total_xp = models.IntegerField()
    upgrades = models.JSONField()
    week = models.IntegerField(default=config.CONFIG_SEASON["CURRENT_WEEK"])
    season = models.IntegerField(default=config.CONFIG_SEASON["CURRENT_SEASON"])
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)


class PaymentLog(models.Model):
    """
    A model to store the payment logs for players.
    """

    staff = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE)
    player = models.ForeignKey("players.Player", on_delete=models.CASCADE)
    payment = models.IntegerField()
    reason = models.CharField(max_length=255)
    type = models.CharField(max_length=2)
    week = models.IntegerField(default=config.CONFIG_SEASON["CURRENT_WEEK"])
    season = models.IntegerField(default=config.CONFIG_SEASON["CURRENT_SEASON"])
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Returns a string representation of the PaymentLog instance.
        """

        return f"{self.staff.username} paid {self.player} ${self.payment} {self.type} for {self.reason}"


class ContractLog(models.Model):
    """
    A model to store the contract logs for players.
    """

    player = models.ForeignKey("players.Player", on_delete=models.CASCADE)
    season = models.IntegerField()
    length = models.IntegerField()
    year_2_option = models.CharField(max_length=32, default="None")
    year_3_option = models.CharField(max_length=32, default="None")
    year_1_payment = models.IntegerField()
    year_2_payment = models.IntegerField(default=0)
    year_3_payment = models.IntegerField(default=0)
    no_trade_clause = models.BooleanField(default=False)
    no_release_clause = models.BooleanField(default=False)
    incentives = models.CharField(max_length=255, default="None")
    weeks_paid = models.JSONField(default=dict, null=True, blank=True)
    current_year = models.CharField(
        max_length=32,
        choices=(("Year 1", "Year 1"), ("Year 2", "Year 2"), ("Year 3", "Year 3")),
        default="Year 1",
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Returns a string representation of the ContractLog instance.
        """

        return f"S{self.season} {self.player}"


class ContractOfferLog(models.Model):
    """
    A model to store the contract offer logs for players.
    """

    season = models.ForeignKey("stats.Season", on_delete=models.CASCADE)
    player = models.ForeignKey("players.Player", on_delete=models.CASCADE)
    projected_role = models.CharField(
        max_length=32, choices=config.CONFIG_PLAYER["ROLES"], default="Regular"
    )
    team = models.ForeignKey("teams.Team", on_delete=models.CASCADE)
    length = models.IntegerField()
    year_2_option = models.CharField(max_length=32, default="None")
    year_3_option = models.CharField(max_length=32, default="None")
    year_1_payment = models.IntegerField()
    year_2_payment = models.IntegerField(default=0)
    year_3_payment = models.IntegerField(default=0)
    notes = models.CharField(max_length=255, default="None")
    no_trade_clause = models.BooleanField(default=False)
    no_release_clause = models.BooleanField(default=False)
    verbally_agreed = models.BooleanField(default=False)
    officially_signed = models.BooleanField(default=False)
    confirmation_time = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Returns a string representation of the ContractOfferLog instance.
        """

        return f"{self.player} offer from {self.team} for {self.season}"


class TransactionMoveLog(models.Model):
    """
    A model to store the transaction move logs for players.
    """

    team = models.ForeignKey(
        "teams.Team",
        on_delete=models.CASCADE,
        help_text="The team making the transaction.",
    )
    signed = models.ForeignKey(
        "players.Player",
        on_delete=models.CASCADE,
        related_name="signed",
        help_text="The player being signed.",
    )
    released = models.ForeignKey(
        "players.Player",
        on_delete=models.CASCADE,
        related_name="released",
        help_text="The player being released.",
    )
    approved = models.BooleanField(
        default=False, help_text="Whether the transaction has been approved."
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Returns a string representation of the TransactionMoveLog instance.
        """

        return f"{self.team} released {self.released} for {self.signed}"

    def move_players(self):
        """
        Moves the players from one team to another.
        """

        if (self.team and self.released and self.signed) and (
            self.released != self.signed
        ):
            if self.released.team == self.team and self.signed.team is None:
                self.released.team = None
                self.signed.team = self.team
                self.approved = True
                self.released.save()
                self.signed.save()
                self.save()

    def save(self, *args, **kwargs):
        """
        Saves the TransactionMoveLog instance and moves the players if not approved.
        """

        if not self.approved:
            self.move_players()
            super(TransactionMoveLog, self).save(*args, **kwargs)


class TrophyLog(models.Model):
    """
    A model to store the trophy logs for players.
    """

    player = models.ForeignKey("players.Player", on_delete=models.CASCADE)
    trophy = models.CharField(max_length=32, choices=config.CONFIG_PLAYER["TROPHIES"])
    season = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Returns a string representation of the TrophyLog instance.
        """

        return f"{self.player} won {self.trophy} in S{self.season}"
