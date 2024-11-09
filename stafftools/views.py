# Django imports
from django.core.management import call_command
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views import View
from django.shortcuts import render

# Local imports
from accounts.models import CustomUser
from logs.models import PaymentLog
from players.models import Player
from teams.models import Team
from stafftools.models import PaymentRequest
from stats.models import PlayerSeasonStats, TeamSeasonStats
from simulation.payment import Payment, pay_contracts
from simulation.webhook import send_webhook

# Create your views here.

# A function that handles the payment of a player
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

# A function that handles the bulk payment of players
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

# A class that handles the bulk payment of players
class BulkPayView(View):
    template_name = "stafftools/bulk_pay.html"

    def get(self, request):
        # Check staff status
        if not request.user.can_pay_players:
            return HttpResponse("You are not authorized to bulk pay users.")
        # Render the template
        return render(request, self.template_name, {"players": Player.objects.values("id", "first_name", "last_name")})

# A class that handles the bulk assignment of players to teams
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

# A class that handles the refreshing of statistics
class RefreshStatsView(View):
    template_name = "stafftools/refresh_stats.html"

    def get(self, request):
        # Check staff status
        if not request.user.is_superuser:
            return HttpResponse("You are not authorized to refresh statistics.")
        # Render the template
        return render(request, self.template_name)

    def post(self, request):
        # Check staff status
        if not request.user.is_superuser:
            return HttpResponse("You are not authorized to refresh statistics.")
        # Update the team and player stats
        refresh_result = "📊 Refresh Results 📊<br>"
        team_season_stats = TeamSeasonStats.objects.all()
        player_season_stats = PlayerSeasonStats.objects.all()
        for season_stats in team_season_stats:
            refresh_result += f"{season_stats.team.city} {season_stats.team.name}<br>"
            season_stats.save()
        for season_stats in player_season_stats:
            refresh_result += f"{season_stats.player.first_name} {season_stats.player.last_name}<br>"
            season_stats.save()
        # Return the response
        return HttpResponse(f"{refresh_result}")
    
# A class that handles the request payment form
class PaymentRequestView(View):
    template_name = "stafftools/payment_request.html"

    def get(self, request):
        user = request.user
        player_list = Player.objects.filter(user=user)
        staff_members = CustomUser.objects.filter(can_pay_players=True)
        return render(request, self.template_name, {"players": player_list, "staff_members": staff_members})

    def post(self, request):
        # Grab the form data
        player = request.POST.get("request-player")
        request_sp_amount = request.POST.get("request-sp-amount")
        request_xp_amount = request.POST.get("request-xp-amount")
        request_reason = request.POST.get("request-reason")
        request_staff = request.POST.get("request-staff")
        # Check how many requests the user has made
        print("Staff:", request_staff) # Debugging
        staff = CustomUser.objects.get(pk=request_staff)
        player = Player.objects.get(pk=player)
        request_count = PaymentRequest.objects.filter(player=player).count()
        # Validate the form data
        if not staff or not player or not request_sp_amount or not request_xp_amount or not request_reason:
            return HttpResponse("❌ All fields are required.")
        # Check if the user has made more than 3 requests
        if request_count > 3:
            return HttpResponse("😊 Please allow us to settle your other payment requests first.")
        # Create the payment request
        PaymentRequest.objects.create(
            player=player, 
            sp_amount=request_sp_amount,
            xp_amount=request_xp_amount,
            reason=request_reason,
            staff=staff,
        )
        # Return the response
        return HttpResponse("✅ Payment has been requested, we'll get back to you soon!")

# A class that handles paying out the payment requests
class PaymentRequestsView(View):
    template_name = "stafftools/payment_requests.html"

    def get(self, request):
        # Check staff status
        if not request.user.can_pay_players:
            return HttpResponse("You are not authorized to pay out requests.")
        # Get all payment requests
        open_requests = PaymentRequest.objects.filter(staff=request.user)
        return render(request, self.template_name, {"open_requests": open_requests})

    def post(self, request):

        # Check staff status
        if not request.user.can_pay_players:
            return HttpResponse("You are not authorized to pay out requests.")
        # Grab the form data
        open_requests = PaymentRequest.objects.filter(staff=request.user)
        # Validate that there are any open requests
        if not open_requests:
            return HttpResponse("❌ There are no open requests.")
        # Check checkbox from each card in template
        result = "<h1>Payout Results</h1><hr>"
        for open_request in open_requests:
            # Get some data from the form
            sp_amount = request.POST.get(f"sp-{open_request.id}")
            xp_amount = request.POST.get(f"xp-{open_request.id}")
            reason = request.POST.get(f"reason-{open_request.id}")
            process_request = request.POST.get(f"process-{open_request.id}")
            delete_request = request.POST.get(f"delete-{open_request.id}")
            # Validate the form data
            if not sp_amount or not xp_amount or not reason:
                result += f"❌ Please fill out all fields for request #{open_request.id}.<br>"
            if not process_request and not delete_request:
                continue # Skip to the next open request
            # Process the payment or delete the request
            if delete_request == "on":
                result += f"❌ Deleted request #{open_request.id} worth {open_request.sp_amount} SP and {open_request.xp_amount} XP for {open_request.player.first_name} {open_request.player.last_name}.<br>"
                open_request.delete() # Delete the request
            elif process_request == "on":
                # Initialize the payment instance (pays player, restricts to limit, & logs payment)
                payment_obj = Payment(
                    payer=request.user,
                    receiver=open_request.player,
                    amount=0,
                    reason=f"[REQUESTED] {reason}",
                    include_xp_equivalent=False,
                )
                # Log the payment
                if int(sp_amount) > 0:
                    payment_obj.amount = int(sp_amount)
                    result += payment_obj.pay_sp() # Pay the SP (returns success/error string)
                if int(xp_amount) > 0:
                    payment_obj.amount = int(xp_amount)
                    result += payment_obj.pay_xp() # Pay the XP (returns success/error string)
                # Send a discord webhook
                send_webhook(
                    url="payment_requests",
                    title="Payment Request Processed",
                    body=f"Payment request for {open_request.player.first_name} {open_request.player.last_name} has been processed.",
                    fields=[
                        ("SP Paid", sp_amount),
                        ("XP Paid", xp_amount),
                        ("Staff Reason", reason),
                        ("Staff Member", open_request.staff.username),
                    ],
                )
                # Delete the request
                open_request.delete()
        # Return the response
        return HttpResponse(result)
