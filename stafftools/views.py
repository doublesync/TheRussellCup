# Django imports
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

# Local imports
from accounts.models import CustomUser
from logs.models import PaymentLog
from players.models import Player
from teams.models import Team
from simulation.payment import Payment, pay_contracts

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

@login_required
def pay_auto_collections(request):
    # Check staff status
    if not request.user.can_pay_players:
        return HttpResponse("You are not authorized to pay users.")
    # Make the function to pay players
    # Get all players that have has_care_package set to True
    users = CustomUser.objects.filter(has_care_package=True)
    response = "💸 Auto Collection Results 💸<br>"
    # Run Payment.pay_contracts for each player
    for user in users:
        result = pay_contracts(user)
        response += f"{user.username}: {result}<br>" 
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
    
class BulkAssignTeamView(View):
    template_name = "stafftools/bulk_assign_team.html"

    def get(self, request):
        # Check staff status
        if not request.user.is_superuser:
            return HttpResponse("You are not authorized to bulk assign users.")
        # Create the context & render the template
        context = {
            "players": Player.objects.values("id", "first_name", "last_name"),
            "teams": Team.objects.all(),
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        # Check staff status
        if not request.user.is_superuser:
            return HttpResponse("You are not authorized to bulk assign users to teams.")
        # Grab the form data
        assign_list = request.POST.getlist("assign-list")
        assign_team = request.POST.get("assign-team")
        clear_existing_members = request.POST.get("clear-existing-members")
        # Clear the existing members if the field is checked
        team = Team.objects.get(pk=assign_team)
        if clear_existing_members == "on":
            for player in team.player_set.all():
                player.team = None
                player.save()
        # Assign the players to the team
        for id in assign_list:
            player = Player.objects.get(pk=id)
            player.team = team
            player.save()
            
        # Return the response
        return HttpResponse("✅ Players have been assigned to the team.")