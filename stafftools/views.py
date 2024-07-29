# Django imports
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

# Local imports
from accounts.models import CustomUser
from logs.models import PaymentLog
from players.models import Player
from simulation.payment import Payment

# Create your views here.
@login_required
def pay_user(request, id, payment_type):
    if request.method == "POST":
        # Check staff status
        if not request.user.can_pay_players:
            return HttpResponse("You are not authorized to pay users.")
        # Make the function to pay players
        def setup_payment(player):
            amount = int(request.POST.get("pay-amount")) or 0 # Default to 0
            currency = request.POST.get("pay-currency")
            reason = request.POST.get("pay-reason")
            _type = request.POST.get("pay-type")
            include_xp_equivalent = request.POST.get("include-xp-equivalent")
            # Update the player's balance
            if amount and currency == "SP":
                amount = int(amount) if _type == "add" else (0 - abs(int(amount)))
            if amount and currency == "XP":
                amount = int(amount) if _type == "add" else (0 - abs(int(amount)))
            # Create the payment
            payment = Payment(request.user, player, amount, reason, include_xp_equivalent)
            response = payment.pay_sp() if currency == "SP" else payment.pay_xp()
            return response
        # Grab the form data
        if payment_type == "bulk":
            response = ""
            pay_list = request.POST.getlist("pay-list")
            for id in pay_list:
                player = Player.objects.get(pk=id)
                response += setup_payment(player)
        else:
            player = Player.objects.get(pk=id)
            response = setup_payment(player)
        # Return the response
        return HttpResponse(response)

class BulkPayView(View):
    template_name = "stafftools/bulk_pay.html"

    def get(self, request):
        # Check staff status
        if not request.user.is_superuser:
            return HttpResponse("You are not authorized to bulk pay users.")
        # Render the template
        return render(request, self.template_name, {"players": Player.objects.values("id", "first_name", "last_name")})