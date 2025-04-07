# Python imports
from datetime import timedelta
from django.utils import timezone

# Django imports
from django.core.management import call_command
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import render
from django.template.loader import render_to_string

# Local imports
from django_project.decorators import check_free_agency_open
from accounts.models import CustomUser
from logs.models import PaymentLog, ContractLog, ContractOfferLog
from players.models import Player
from teams.models import Team, get_managed_team
from stafftools.models import PaymentRequest
from stats.models import Season, PlayerSeasonStats, TeamSeasonStats
from simulation.payment import Payment, pay_contracts
from simulation.webhook import send_webhook
from simulation import config
from simulation import artificial

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
        if not request.user.is_staff:
            return HttpResponse("You are not authorized to bulk assign users.")
        # Create the context & render the template
        context = {
            "players": Player.objects.values("id", "first_name", "last_name"),
            "teams": Team.objects.all(),
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        # Check staff status
        if not request.user.is_staff:
            return HttpResponse("You are not authorized to bulk assign users to teams.")
        # Grab the form data
        assign_team = request.POST.get("assign-team")
        assign_list = request.POST.getlist("assign-list")
        remove_list = request.POST.getlist("remove-list")
        remove_all = request.POST.get("remove-all")
        team = Team.objects.get(pk=assign_team)
        # Remove all players from the team
        if remove_all == "on":
            team.player_set.all().update(team=None)
        # Assign the players to the team
        for id in assign_list:
            player = Player.objects.get(pk=id)
            player.team = team
            player.save()
        # Remove the players from the team
        if remove_all != "on":
            for id in remove_list:
                player = Player.objects.get(pk=id)
                player.team = None
                player.save()
        # Return the response
        return HttpResponse("✅ Changes were successfully made.")

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

# This is a class based view that will allow managers to send contract offers to players
class OfferContractsView(View):
    
    @method_decorator(check_free_agency_open)
    def get(self, request):
        context = {
            "players": Player.objects.all(),
            "teams": Team.objects.all(),
            "roles": config.CONFIG_PLAYER["ROLES"],
        }
        return render(request, "stafftools/offer_contracts.html", context)
    
    def validate(self, request):
    
        # Validate user (manager)
        team = get_managed_team(request.user)
        if not team:
            return render(request, "500.html", {"reason": "You are not a team manager, or manage multiple teams."})

        # Fetch the form values
        offer_list = request.POST.getlist("offer-list")
        projected_role = request.POST.get("projected-role")
        year_one_salary = request.POST.get("year-one-salary")
        year_two_salary = request.POST.get("year-two-salary")
        year_three_salary = request.POST.get("year-three-salary")
        year_two_option = request.POST.get("year-two-option")
        year_three_option = request.POST.get("year-three-option")
        no_trade_clause = request.POST.get("no-trade-clause")
        no_release_clause = request.POST.get("no-release-clause")
        contract_notes = request.POST.get("contract-notes")

        # Post-process form values
        contract_length = bool(year_one_salary) + bool(year_two_salary) + bool(year_three_salary)
        year_one_salary = int(year_one_salary) if year_one_salary else None
        year_two_salary = int(year_two_salary) if year_two_salary else None
        year_three_salary = int(year_three_salary) if year_three_salary else None
        no_trade_clause = True if no_trade_clause == "on" else False
        no_release_clause = True if no_release_clause == "on" else False
        projected_role = projected_role or "Regular"
        contract_notes = contract_notes or "No notes provided."

        # Validate some form values
        if (year_one_salary and year_one_salary > 600) or (year_two_salary and year_two_salary > 600) or (year_three_salary and year_three_salary > 600):
            messages.error(request, "❌ The maximum salary is $600.")
        if year_three_salary and not year_two_salary:
            messages.error(request, "❌ Year 3 salary cannot be set without a Year 2 salary.")
        if year_two_salary and not year_one_salary:
            messages.error(request, "❌ Year 2 salary cannot be set without a Year 1 salary.")
        if not year_one_salary:
            messages.error(request, "❌ Year 1 salary is required.")
        if not offer_list:
            messages.error(request, "❌ No players were selected.")       
        if not year_two_salary:
            year_two_option = "None"
        if not year_three_salary:
            year_three_option = "None"

        # Return validated values
        return {
            "team": team,
            "offer_list": offer_list,
            "projected_role": projected_role,
            "year_one_salary": year_one_salary,
            "year_two_salary": year_two_salary,
            "year_three_salary": year_three_salary,
            "year_two_option": year_two_option,
            "year_three_option": year_three_option,
            "contract_length": contract_length,
            "no_trade_clause": no_trade_clause,
            "no_release_clause": no_release_clause,
            "contract_notes": contract_notes,
        }
    
    @method_decorator(check_free_agency_open)
    def post(self, request):
        if request.method == "POST":
            # Get validated form values
            validated_values = self.validate(request)
            team = validated_values.get("team")
            offer_list = validated_values.get("offer_list")
            projected_role = validated_values.get("projected_role")
            year_one_salary = validated_values.get("year_one_salary")
            year_two_salary = validated_values.get("year_two_salary")
            year_three_salary = validated_values.get("year_three_salary")
            year_two_option = validated_values.get("year_two_option")
            year_three_option = validated_values.get("year_three_option")
            contract_length = validated_values.get("contract_length")
            no_trade_clause = validated_values.get("no_trade_clause")
            no_release_clause = validated_values.get("no_release_clause")
            contract_notes = validated_values.get("contract_notes")

            # Create the contract offer(s)
            season = Season.objects.filter(current_season=True).first()
            for player_id in offer_list:
                player = Player.objects.get(pk=player_id)
                if player:
                    # Check if team has existing offer to player before creating contract
                    team_offered_already = ContractOfferLog.objects.filter(team=team, player=player, season=season).exists()
                    if team_offered_already:
                        messages.error(request, f"❌ {player.first_name} {player.last_name} already has an offer from {team.city} {team.name}.")
                        continue
                    # Create the contract if team doesn't have an offer out already
                    contract_offer = ContractOfferLog.objects.create(
                        season=season,
                        player=player,
                        projected_role=projected_role,
                        team=team,
                        length=contract_length,
                        year_2_option=year_two_option,
                        year_3_option=year_three_option,
                        year_1_payment=year_one_salary,
                        no_trade_clause=no_trade_clause,
                        no_release_clause=no_release_clause,
                        notes=contract_notes,
                    )
                    if year_two_salary:
                        contract_offer.year_2_payment = year_two_salary
                    if year_three_salary:
                        contract_offer.year_3_payment = year_three_salary
                    contract_offer.save()
                    messages.success(request, f"✅ {player.first_name} {player.last_name} has been offered a contract by {team.city} {team.name}.")

            # Redirect/refresh the page
            return HttpResponseRedirect(reverse('offer_contracts'))

# This is a class based view that will allow managers to view, and delete contract offers
class ViewOffersView(View):

    @method_decorator(check_free_agency_open)
    def get(self, request):
        # Validate user (manager)
        team = get_managed_team(request.user)
        if not team:
            return render(request, "500.html", {"reason": "You are not a team manager, or manage multiple teams."})
        # Fetch all the contract offers made by the team
        season = Season.objects.filter(current_season=True).first()
        offers = ContractOfferLog.objects.filter(season=season, team=team)
        context = {
            "team": team,
            "offers_sent": offers,
        }
        return render(request, "stafftools/view_offers.html", context)

# This is a class based view that allows players to see their offers
class ViewPlayerOffersView(View):

    @method_decorator(check_free_agency_open)
    def get(self, request):
        # Find user players
        players = Player.objects.filter(user=request.user)
        # Find all offers for players
        offers = ContractOfferLog.objects.filter(player__in=players)
        # Create context
        context = {
            "offers_sent": offers, # offers_sent is really offers_received here; but we are re-using the same template
        }
        # Render the template
        return render(request, "stafftools/view_player_offers.html", context)

# This is a function based htmx view that will allow managers to withdraw contract offers
# This function works both for managers withdrawing offers, and players declining offers
@check_free_agency_open
def htmx_withdraw_offers(request, return_type):
    if request.method == "POST":
        # Validate user (manager)
        team = get_managed_team(request.user)

        # Grab withdraw list offers from the form
        withdraw_list = request.POST.getlist("withdraw-list")
        # Check if the list is empty
        if not withdraw_list:
            messages.info(request, "❌ No offers were selected.")
            return HttpResponse(None, headers={"HX-Redirect": request.META.get("HTTP_REFERER")})

        # Withdraw the offers
        for id in withdraw_list:
            # Check if the offer exists
            offer_exists = ContractOfferLog.objects.filter(pk=id).exists()
            if offer_exists:
                # Find the offer
                offer = ContractOfferLog.objects.get(pk=id)
                # TODO: Keep an eye out on this
                # Check if the offer has been verbally agreed to and the offer's confirmation time has passed, or if the offer has been officially signed
                if (offer.verbally_agreed and offer.confirmation_time < timezone.now()) or offer.officially_signed:
                    messages.error(request, "❌ This offer has already been finalized.")
                    return HttpResponse(None, headers={"HX-Redirect": request.META.get("HTTP_REFERER")})
                # Check if the user manages the team that amde the offer, or owns the player that was offered
                # This logic combines team withdrawals and player withdrawals into one function
                if (request.user != offer.player.user) and (offer.team != team):
                    messages.error(request, "❌ You do not manage the offering team, or own the offered player.")
                    return HttpResponse(None, headers={"HX-Redirect": request.META.get("HTTP_REFERER")})
                else:
                    offer.delete()

        # Redirect/refresh the page
        season = Season.objects.filter(current_season=True).first()
        # Initialize the offers_sent variable
        offers_sent = ContractOfferLog.objects.filter(season=season)
        # If the offer is being 'declined' by the player, return the list of offers for players
        if return_type == "return_players":
            players = Player.objects.filter(user=request.user)
            offers_sent = offers_sent.filter(player__in=players)
            messages.info(request, "🔎 Showing offers for players owned by you.")
        else:
            # If the offer is being 'withdrawn' by the team, return the list of offers for teams
            offers_sent = offers_sent.filter(team=team)
            messages.info(request, f"🔎 Showing offers made by {team}.")

        # Build the context
        # TODO: Make the countdowns update aswell when an offer is withdrawn
        context = {
            "team": team,
            "offers_sent": offers_sent,
        }
        html = render_to_string("stafftools/fragments/offers_table.html", context)
        return HttpResponse(html)
    
# This is a function based view that will allow players to accept contract offers
@check_free_agency_open
def htmx_accept_offer(request, offer_id):
    if request.method == "POST":
        # Validate user owns player
        offer = ContractOfferLog.objects.get(pk=offer_id)
        if request.user != offer.player.user or offer.player.team != None:
            messages.error(request, "❌ You do not own this player, or the player is already on a team.")
            return HttpResponse(None, headers={"HX-Redirect": request.META.get("HTTP_REFERER")})
        
        # Validate the offer is not already verbally or officially signed
        if offer.verbally_agreed or offer.officially_signed:
            messages.error(request, "❌ This offer has already been agreed to.")
            return HttpResponse(None, headers={"HX-Redirect": request.META.get("HTTP_REFERER")})
        
        # TODO: Keep an eye out on this
        # Check if the player has any verbally-agreed-to offers with the confirmation time in the past, or if they have any officially-agreed-to offers
        verbally_agreed_offers = ContractOfferLog.objects.filter(player=offer.player, verbally_agreed=True, confirmation_time__lte=timezone.now())
        officially_agreed_offers = ContractOfferLog.objects.filter(player=offer.player, officially_signed=True)
        if verbally_agreed_offers.exists() or officially_agreed_offers.exists():
            messages.error(request, "❌ You already have an offer that is finalized.")
            return HttpResponse(None, headers={"HX-Redirect": request.META.get("HTTP_REFERER")})

        # Update the offer to be verbally signed
        offer.verbally_agreed = True
        offer.confirmation_time = timezone.now() + timedelta(hours=8)
        offer.save()

        # Set all other contracts 'verbally_agreed' to False
        ContractOfferLog.objects.filter(player=offer.player, season=offer.season).exclude(pk=offer.pk).update(verbally_agreed=False)

        # Send a discord webhook with an ai-generated message (similar to Shams or Woj)
        signing_tweet = artificial.prompt_signing_tweet(offer)
        send_webhook(
            url="breaking_news",
            title="",
            body=signing_tweet,
        )

        # Send a success message & refresh the page
        messages.success(request, "✅ You have verbally agreed to this offer.")
        return HttpResponse(None, headers={"HX-Redirect": request.META.get("HTTP_REFERER")})
