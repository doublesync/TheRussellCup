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
        # Validate the form data
        if _type not in ["SP", "XP"]:
            return HttpResponse(f"❌ Invalid currency type? {currency}")
        # Update the player's balance
        if amount and currency == "SP":
            amount = int(amount) if _type == "add" else (0 - abs(int(amount)))
            player.user.sp += amount
        if amount and currency == "XP":
            amount = int(amount) if _type == "add" else (0 - abs(int(amount)))
            player.user.xp += amount
        player.user.save()
        # Create the payment log
        PaymentLog.objects.create(
            staff=request.user,
            player=player,
            payment=amount,
            reason=reason,
            type=currency,
        )
        # Return the response
        return HttpResponse("✅ Payment successful.")
