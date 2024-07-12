# Python imports

# Django imports
from django.db import models

# Local imports
import simulation.config as config
from logs.models import PaymentLog


# A class to handle payments
class Payment:
    
    def __init__(self, payer, receiver, amount, reason, bypass=False):
        self.payer = payer
        self.receiver = receiver
        self.amount = amount
        self.reason = reason
        self.bypass = bypass

    def exceeds_limit(self, adding_amount):
        # Filter payments for the current season (only) and sum them up
        total_payment = PaymentLog.objects.filter(
            player=self.receiver, 
            season=config.CONFIG_SEASON["CURRENT_SEASON"],
            type="SP").aggregate(models.Sum("payment"))["payment__sum"] or 0
        # Check if the total payment plus the adding amount would surpass the maximum allowed
        if (total_payment + adding_amount) > config.CONFIG_SEASON["MAX_SP_SEASON"]:
            return True
        # Return False if the payment would not surpass the maximum
        return False
    
    def pay_sp(self):
        # Validate the payment amount
        if self.exceeds_limit(self.amount):
            return "❌ Payment would surpass the maximum allowed for the season."
        # Create the payment log
        PaymentLog.objects.create(
            staff=self.payer, 
            player=self.receiver, 
            payment=self.amount, 
            reason=self.reason, 
            type="SP"
        )
        # Send the player/user's payment
        self.receiver.user.sp += self.amount
        self.receiver.user.save()
        # Return True since the payment was successful
        return "✅ Payment successful."
    
    def pay_xp(self):
        # Create the payment log
        PaymentLog.objects.create(
            staff=self.payer, 
            player=self.receiver, 
            payment=self.amount, 
            reason=self.reason, 
            type="XP"
        )
        # Send the player/user's payment
        self.receiver.user.xp += self.amount
        self.receiver.user.save()
        # Return True since the payment was successful
        return True

# A method that pays a user's players based on their contract
def pay_contracts(user):
    # Get the user's players
    players = user.player_set.all()
    current_week = config.CONFIG_SEASON["CURRENT_WEEK"]
    players_paid = []
    # Loop through the players
    if players:
        for player in players:
            if player.contract:
                if player.contract.weeks_paid and (str(current_week) in player.contract.weeks_paid):
                    # If we allow multiple players, we'll need to change this to a list
                    return "❌ Players have already been paid for this week."
                else:
                    # Pay the player
                    player.user.sp += round(player.contract.current_year_payment * 0.30)
                    player.user.sp += config.CONFIG_SEASON["CHECKIN_SP"]
                    player.user.xp += round(player.contract.current_year_payment * 0.70)
                    player.user.xp += config.CONFIG_SEASON["CHECKIN_XP"]
                    player.user.save()
                    # Update the player's contract
                    if player.contract.weeks_paid:
                        player.contract.weeks_paid[current_week] = True
                    else:
                        player.contract.weeks_paid = {current_week: True}
                    player.contract.save()
                    players_paid.append(player)
    # Return success message since the payment was successful
    return f"✅ Players paid: {players_paid}"

# A method that counts the total salary cap spent for a team
def get_salary_book(team):
    # Get the team's players
    players = team.player_set.all()
    salary_book = {"total_spent": 0}
    # Loop through the players
    for player in players:
        if player.contract:
            salary_book[player.id] = player.contract.current_year_payment
            salary_book["total_spent"] += player.contract.current_year_payment
    # Return the total spent
    return salary_book