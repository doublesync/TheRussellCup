# Django imports
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

# Local imports
from accounts.models import CustomUser
from logs.models import PaymentLog
from players.models import Player
from simulation.payment import Payment

# Create your views here.
@login_required
def pay_user(request, id):
    if request.method == "POST":
        # Check staff status
        if not request.user.can_pay_players:
            return HttpResponse("You are not authorized to pay users.")
        # Grab the form data
        player = Player.objects.get(pk=id)
        amount = request.POST.get("pay-amount")
        currency = request.POST.get("pay-currency")
        reason = request.POST.get("pay-reason")
        _type = request.POST.get("pay-type")
        # Update the player's balance
        if amount and currency == "SP":
            amount = int(amount) if _type == "add" else (0 - abs(int(amount)))
        if amount and currency == "XP":
            amount = int(amount) if _type == "add" else (0 - abs(int(amount)))
        # Create the payment
        payment = Payment(request.user, player, amount, reason)
        response = payment.pay_sp() if currency == "SP" else payment.pay_xp()
        # Return the response
        return HttpResponse(response)
