# Python imports
import json

# Django imports
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.views.generic.edit import FormView
from django.views.generic.base import View
from django.views.generic.list import ListView

# Local imports
from players.models import Player, Modification
from players.forms import PlayerForm, UpgradeForm
from stats.models import Season, PlayerSeasonStats, TeamSeasonStats
import simulation.statfinder as statfinder
import simulation.artificial as ai
import simulation.create as create
import simulation.upgrade as upgrade
import simulation.modification as modification
import simulation.scripts.attribute as attribute
import simulation.scripts.badge as badge
import simulation.scripts.tendency as tendency
import simulation.scripts.sorting as sorting


# This is a class based view that will render the form to create a player
class PlayerFormView(FormView):

    template_name = "players/create_player.html"
    form_class = PlayerForm
    success_url = "/"

    def form_valid(self, form):
        data = form.cleaned_data
        seed = create.PlayerCreator(
            first_name=data["first_name"],
            last_name=data["last_name"],
            position=data["position"],
            number=data["number"],
            country=data["country"],
            college=data["college"],
            user=self.request.user,
        )
        # Create the player (or return an error message if the player is invalidated)
        player = seed.create()
        if type(player) == str:
            messages.error(self.request, player)
            return render(self.request, self.template_name, {"form": form})
        else:
            # Redirect to the player page
            return redirect(player_page, id=player.id)


# This is a function based view that will render the player page
@login_required
def player_page(request, id):
    # fmt:off
    player = Player.objects.get(pk=id)
    sorted_attributes = attribute.order_attributes(player.attributes)
    sorted_badges = badge.order_badges(player.badges)
    sorted_tendencies = tendency.order_tendencies(player.tendencies)
    return render(request, "players/player_page.html", {
        "user": request.user,
        "player": player, 
        "attributes": sorted_attributes, 
        "badges": sorted_badges,
        "tendencies": sorted_tendencies,
        "attribute_categories": attribute.attribute_categories,
        "badge_categories": badge.badge_categories,
        "tendency_categories": tendency.tendency_categories
    })
    # fmt:on


# This is a class based view that will render the form to upgrade a player
class UpgradeFormView(FormView):

    # fmt: off

    template_name = "players/upgrade_player.html"
    form_class = UpgradeForm

    def get(self, request, *args, **kwargs):
        player_id = self.kwargs.get("id")
        player = Player.objects.get(pk=player_id)
        if player.user != request.user:
            return render(request, "500.html", {"reason": "You do not own this player"})
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        player_id = self.kwargs.get("id")
        player = Player.objects.get(pk=player_id)
        context.update(
            {
                "player": player,
                "form": UpgradeForm(player=player),
                "attribute_categories": attribute.attribute_categories,
                "badge_categories": badge.badge_categories,
                "tendency_categories": tendency.tendency_categories,
            }
        )
        return context

    def form_valid(self, form):
        # If the user updated their cart (we send an HX request)
        if self.request.headers.get("HX-Request") == "true":
            # Initialize some objects
            original_attributes = json.loads(self.request.POST.get("original_attributes").replace("'", '"'))
            original_badges = json.loads(self.request.POST.get("original_badges").replace("'", '"'))
            original_tendencies = json.loads(self.request.POST.get("original_tendencies").replace("'", '"'))
            original_player = {
                "attributes": original_attributes,
                "badges": original_badges,
                "tendencies": original_tendencies,
            }
            # Get 'validate_price's return cart dictionary and render the cart fragment
            upg = upgrade.UpgradeCreator(user=self.request.user, player=original_player, data=form.data)
            cart = upg.validate_price(validate=False)[1]
            html = render_to_string("players/fragments/cart_fragment.html", {"cart": cart})
            return HttpResponse(html)
        # If the user submitted the form (we send a POST request without HX)
        else:
            # Initialize some objects
            player = Player.objects.get(pk=form.data["player_id"])
            upg = upgrade.UpgradeCreator(user=self.request.user, player=player, data=form.data)
            purchase_status, purchase_response = upg.purchase()
            # If the purchase was successful, display a success message
            if purchase_status:
                messages.success(self.request, purchase_response)
            else:
                # If there are errors, display them all
                for error in purchase_response:
                    messages.error(self.request, error)
            # Redirect to the player page
            return redirect("upgrade_page", id=player.id)

    # fmt: on


# This is a list based view that will render the player list
class PlayerListView(ListView):

    # Sends 'page_obj' to the template

    model = Player
    template_name = "players/player_list.html"
    context_object_name = "players"
    paginate_by = 10

    def get_queryset(self):
        return Player.objects.all().order_by("-sim_rating")


# This is a function based view that will render a filtered player list
def htmx_filter_players(request, model):
    
    # Initialize some objects
    model_sorting = model
    fragment_name = None
    query_function = None
    selected_season = request.POST.get("selected-season")
    if selected_season == "all_seasons":
        selected_season_object = None
    else:
        selected_season_object = Season.objects.filter(season=selected_season).first()
    # Determine the model and query function
    if model == "players":
        model_sorting = Player
        fragment_name = "players/fragments/list_fragment.html"
        query_function = sorting.build_player_list_params
    elif model == "stats":
        model_sorting = PlayerSeasonStats
        fragment_name = "stats/fragments/list_fragment.html"
        query_function = sorting.build_averages_list_params
    # Get the page & query from our custom query builder
    page = request.GET.get("page")
    params, query = query_function(request)
    # Check if we are filtering by PlayerSeasonStats or Player
    if model_sorting == PlayerSeasonStats:
        if selected_season_object is None:
            finder = statfinder.StatFinder()
        else:
            finder = statfinder.StatFinder(specific_season=selected_season_object)
        order_by_str = f"{params.order_direction}{params.ordering}"
        player_list = finder.all_player_stats(query=query, order_by=order_by_str)
    else:
        player_list = model_sorting.objects.filter(query).order_by(f"{params.order_direction}{params.ordering}")
    # Paginate the page
    paginator = Paginator(player_list, 10)
    players = paginator.get_page(page)
    # Return the page
    context: dict = {"page_obj": players}
    html: str = render_to_string(fragment_name, context) # Render a fragment based on what HTMX requested
    return HttpResponse(html)


# This is a class based view that will render the edit appearance page
class EditAppearanceView(View):

    def get(self, request, id):
        # Grab the player
        player = Player.objects.get(pk=id)
        # Check if the player belongs to the user
        if player.user != request.user:
            return render(request, "500.html", {"reason": "You do not own this player"})
        # Render the page
        return render(request, "players/edit_appearance.html", {"player": player})
    
    def post(self, request, id):
        # Grab the player
        player = Player.objects.get(pk=id)
        # Check if the player belongs to the user
        if player.user != request.user:
            return render(request, "500.html", {"reason": "You do not own this player"})
        # Update the player's appearance
        svg_image = request.POST.get("face")
        player.svg_image = svg_image
        player.save()
        # Redirect to the player page
        # HX-REDIRECT
        return HttpResponse("Successful! Redirecting...", headers={"HX-Redirect": f"/players/player/{player.id}/"})


# This is a class based view that will render the modifications list
class ModificationsListView(ListView):

    model = Player
    template_name = "players/modifications_list.html"
    context_object_name = "modifications"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        kwargs["players"] = Player.objects.filter(user=self.request.user)
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        return Modification.objects.all().order_by("created")
    

# This is a function based view that will allow the user to purchase a modification
def purchase_modification(request, id):
    # Get the modification
    user = request.user
    mod = Modification.objects.get(pk=id)
    player_id = request.POST.get("mod-player")
    player = Player.objects.get(pk=player_id)
    existing_mods = player.modifications
    # Calculate the price of the modification
    mod_xp_price = mod.xp_price_with_discount if user.has_care_package else mod.xp_price
    # Validate some conditions
    if player.user != user: 
        return None
    if user.xp < mod_xp_price:
        return HttpResponse("❌ You do not have enough XP to purchase this modification")
    if existing_mods and mod.item in existing_mods and not mod.multi_buy:
        return HttpResponse("❌ You already own this modification")
    # Purchase the modification
    if player.modifications:
        count = player.modifications.get(mod.item, 0)
        player.modifications[mod.item] = count + 1
    else:
        player.modifications = {mod.item: 1}
    # Update the player and user XP & XP spent
    user.xp -= mod_xp_price
    player.xp_spent += mod_xp_price
    # Check for a modification function (automatic modifications)
    function = modification.check_for_function(mod.item)
    if function:
        player, message = function(player)
    else:
        message = f"✅ {mod.item} purchased successfully"
    # Save the player and user
    player.save()
    user.save()
    # Return a success message
    return HttpResponse(message)


# This is a function based view that will allow the user to get upgrade advice from GPT-4o
def htmx_upgrade_advice(request, id):
    # Get the player
    player = Player.objects.get(pk=id)
    # Check if the player belongs to the user
    if player and player.user != request.user:
        return render(request, "500.html", {"reason": "You do not own this player or the player does not exist"})
    # Initialize the prompt
    response = ai.prompt_upgrade_advice(player)
    # Return the response
    return HttpResponse(response)