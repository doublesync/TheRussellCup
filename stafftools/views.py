# Django imports
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

# Local imports
from accounts.models import CustomUser
from logs.models import PaymentLog
from players.models import Player

# Create your views here.
@login_required
def pay_user(request, id):
    if request.method == "POST":
        # Check staff status
        if not request.user.is_staff:
            return HttpResponse("You are not authorized to pay users.")
        # Grab the form data
        player = Player.objects.get(pk=id)
        amount = request.POST.get("pay-amount")
        currency = request.POST.get("pay-currency")
        reason = request.POST.get("pay-reason")
        _type = request.POST.get("pay-type")
        # Create the payment log
        PaymentLog.objects.create(
            staff=request.user,
            player=player,
            payment=amount,
            reason=reason,
        )
        # Update the player's balance
        if amount and currency == "SP":
            player.user.sp += int(amount) if _type == "add" else -int(amount)
        if amount and currency == "XP":
            player.user.xp += int(amount) if _type == "add" else -int(amount)
        player.user.save()
        # Return the response
        return HttpResponse("✅ Payment successful.")
