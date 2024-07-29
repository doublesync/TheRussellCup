# Python imports

# Django imports
from django.db import models

# Local imports
import simulation.config as config
from logs.models import PaymentLog, ContractLog


# A class to handle payments
class Payment:
    
    def __init__(self, payer, receiver, amount, reason, include_xp_equivalent, bypass=False):
        self.payer = payer
        self.receiver = receiver
        self.amount = amount
        self.reason = reason
        self.bypass = bypass
        self.include_xp_equivalent = include_xp_equivalent

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
        if not self.receiver.user:
            return f"❌ User not found for {self.receiver.first_name} {self.receiver.last_name}.<br>"
        if self.exceeds_limit(self.amount):
            return f"❌ Payment would surpass the maximum allowed for the season for {self.receiver.first_name} {self.receiver.last_name}.<br>"
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
        if self.include_xp_equivalent == "on":
            self.receiver.user.xp += round((self.amount * 1.7), 0)
        self.receiver.user.save()
        # Return True since the payment was successful
        return f"✅ Payment of {self.amount} SP was successful to {self.receiver.first_name} {self.receiver.last_name}.<br>"
    
    def pay_xp(self):
        if not self.receiver.user:
            return f"❌ User not found for {self.receiver.first_name} {self.receiver.last_name}.<br>"
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
        return f"✅ Payment of {self.amount} XP was successful to {self.receiver.first_name} {self.receiver.last_name}.<br>"

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
                    return "❌ Player/s have already been paid for this week."
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
                    players_paid.append(f"{player.first_name} {player.last_name}")
            else:
                player.contract = ContractLog.objects.create(
                    player=player,
                    season=config.CONFIG_SEASON["CURRENT_SEASON"],
                    length=1,
                    current_year_payment=config.CONFIG_SEASON["DEFAULT_CONTRACT"]
                )
                player.save()
                return f"💴 Contract was created for {player.first_name} {player.last_name}, please try again."
    # Return success message since the payment was successful
    return f"✅ Player/s paid: {players_paid}"

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