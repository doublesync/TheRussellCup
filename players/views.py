import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.views.generic.base import View
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from ipware import get_client_ip

import simulation.config as config
import simulation.create as create
import simulation.modification as modification
import simulation.scripts.accessory as accessory
import simulation.scripts.animation as animation
import simulation.scripts.attribute as attribute
import simulation.scripts.badge as badge
import simulation.scripts.gear as gear
import simulation.scripts.sorting as sorting
import simulation.scripts.tendency as tendency
import simulation.statfinder as statfinder
import simulation.upgrade as upgrade
import simulation.webhook as webhook
from players.forms import PlayerForm, UpgradeForm
from players.models import Modification, Player
from simulation.frivolity import get_girlfriend
from stats.models import PlayerSeasonStats, Season


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
            original_sp_spent = int(self.request.POST.get("original_sp_spent"))
            original_player = {
                "attributes": original_attributes,
                "badges": original_badges,
                "tendencies": original_tendencies,
                "sp_spent": original_sp_spent,
            }
            # Get 'validate_price's return cart dictionary and render the cart fragment
            upg = upgrade.UpgradeCreator(user=self.request.user, player=original_player, data=form.data)
            cart = upg.validate_price(validate=False)[1]
            html = render_to_string("players/fragments/cart_fragment.html", {"cart": cart})
            return HttpResponse(html)
        # If the user submitted the form (we send a POST request without HX)
        else:
            # Grab the IP Address & send it to the discord webhook
            ip, is_routable = get_client_ip(self.request)
            if ip:
                webhook.send_webhook(url="alt_identifier", title=self.request.user.username, body=ip)
            print("IP Address:", ip)
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
        player_list = model_sorting.objects.filter(query).order_by(
            f"{params.order_direction}{params.ordering}"
        )
    # Paginate the page
    paginator = Paginator(player_list, 10)
    players = paginator.get_page(page)
    # Return the page
    context: dict = {"page_obj": players}
    html: str = render_to_string(
        fragment_name, context
    )  # Render a fragment based on what HTMX requested
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
        return HttpResponse(
            "Successful! Redirecting...",
            headers={"HX-Redirect": f"/players/player/{player.id}/"},
        )


# This is a class based view that will render the modifications list
class ModificationsListView(ListView):

    model = Player
    template_name = "players/modifications_list.html"
    context_object_name = "modifications"
    paginate_by = 20

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
    if player.xp < mod_xp_price:
        return HttpResponse(
            "❌ You do not have enough XP to purchase this modification"
        )
    if existing_mods and mod.item in existing_mods and not mod.multi_buy:
        return HttpResponse("❌ You already own this modification")
    # Purchase the modification
    if player.modifications:
        count = player.modifications.get(mod.item, 0)
        player.modifications[mod.item] = count + 1
    else:
        player.modifications = {mod.item: 1}
    # Update the player and user XP & XP spent
    player.xp -= mod_xp_price
    player.xp_spent += mod_xp_price
    # Check for a modification function (automatic modifications)
    function = modification.check_for_function(mod.item)
    if function:
        player, message = function(player)
    else:
        message = f"✅ {mod.item} purchased successfully"
    # Save the player and user
    player.save()
    # Return a success message
    return HttpResponse(message)


# This is a function based view that will allow the user to get upgrade advice from GPT-4o
def htmx_upgrade_advice(request, id):
    # Get the player
    player = Player.objects.get(pk=id)
    # Check if the player belongs to the user
    if player and player.user != request.user:
        return render(
            request,
            "500.html",
            {"reason": "You do not own this player or the player does not exist"},
        )
    # Initialize the prompt
    response = "❌ Upgrade advice is currently disabled."
    # Return the response
    return HttpResponse(response)


# This is a class-based view that will allow the user to see a player's trophy rack
class TrophyRackView(View):

    def get(self, request, id):
        # Get the user's players
        players = Player.objects.get(pk=id)
        # Render the page
        return render(request, "players/trophy_rack.html", {"players": players})


# This is a class-based view that will allow the user to compare two players
class ComparePlayersView(View):

    def get(self, request):
        # Get the user's players
        players = Player.objects.all()
        # Render the page
        return render(request, "players/compare_players.html", {"players": players})


# This is a class-based view that will allow the user to view & change player animations
class PlayerAnimationsView(View):

    def get(self, request, id):
        # Check if the player exists & if the player belongs to the user
        player = get_object_or_404(Player, pk=id)
        if player.user != request.user:
            return render(request, "500.html", {"reason": "You do not own this player"})
        # Get the animation options
        context = {"player": player, "animation_options": animation.animation_options}
        # Render the page
        return render(request, "players/player_animations.html", context)


# This is a class-based view that will allow the user to view & change player accessories and gear
class PlayerStylesView(View):

    def get(self, request, id):
        # Check if the player exists & if the player belongs to the user
        player = get_object_or_404(Player, pk=id)
        if player.user != request.user:
            return render(request, "500.html", {"reason": "You do not own this player"})
        # Get the accessory options
        context = {
            "player": player,
            "accessory_options": accessory.accessory_options,
            "gear_options": gear.gear_options,
        }
        # Render the page
        return render(request, "players/player_styles.html", context)


# This is function based htmx view that will allow the user to change the players being compared
def htmx_compare_players(request):
    if request.method == "POST":
        # Check if the players exist
        player_1 = request.POST.get("player-1")
        player_2 = request.POST.get("player-2")
        # Check if player is being compared to itself
        if not player_1 or not player_2:
            return HttpResponse("❌ You must select two players to compare")
        if player_1 == player_2:
            return HttpResponse(
                f"❌ You cannot compare a player to themselves: ({player_1}) ({player_2})."
            )
        # Check if both players exist
        if (
            not Player.objects.filter(pk=player_1).exists()
            or not Player.objects.filter(pk=player_2).exists()
        ):
            return HttpResponse("❌ One or more of the players do not exist")
        # Get the players
        player_1 = Player.objects.get(pk=player_1)
        player_2 = Player.objects.get(pk=player_2)
        # Create a list of vital fields
        vital_fields = {
            "sp_spent": "SP Spent",
            "xp_spent": "XP Spent",
            "height": "Height",
            "weight": "Weight",
            "wingspan": "Wingspan",
        }
        stat_fields = config.CONFIG_STATS["TRACKED_AVERAGE_FIELDS"]
        # Add player averages to the player objects
        player_1_stats = statfinder.StatFinder().player_stats(player_1)
        player_2_stats = statfinder.StatFinder().player_stats(player_2)
        # Render the page
        return render(
            request,
            "players/fragments/compare_players_fragment.html",
            {
                "player_1": player_1,
                "player_2": player_2,
                "player_1_stats": player_1_stats,
                "player_2_stats": player_2_stats,
                "vital_fields": vital_fields,
                "stat_fields": stat_fields,
            },
        )


# This function based htmx view will allow the user to update the player's styles
def htmx_update_player_styles(request, id):
    # Check if the player exists & if the player belongs to the user
    player = get_object_or_404(Player, pk=id)
    if player.user != request.user:
        return render(request, "500.html", {"reason": "You do not own this player"})
    # Get the accessory & gear data from the request
    accessory_choices = {
        key: value
        for key, value in request.POST.items()
        if key in accessory.accessory_options and value
    }
    gear_choices = {
        key: value
        for key, value in request.POST.items()
        if key in gear.gear_options and value
    }
    # Check if the player has any accessories or gear to update
    updated = False
    for accessory_item, value in accessory_choices.items():
        if player.accessories.get(accessory_item) != value:
            player.accessories[accessory_item] = value
            updated = True
    for gear_item, value in gear_choices.items():
        if player.gear.get(gear_item) != value:
            player.gear[gear_item] = value
            updated = True
    # Only save the player if there were changes made
    if updated:
        player.save()
        messages.success(request, "✅ Player styles updated successfully")
    else:
        messages.info(request, "ℹ️ No changes were made.")
    # Return a refresh with a success message
    return HttpResponse(status=204, headers={"HX-Refresh": "true"})


# This function based htmx view will allow the user to update the player's animations
def htmx_roll_animation(request, id):

    if request.method != "POST":
        return HttpResponse("Invalid request method.")

    player = get_object_or_404(Player, pk=id)
    if player.user != request.user:
        return HttpResponse("❌ You do not own this player.")

    animation_name = request.POST.get("animation_name")
    animation_data = animation.animation_options.get(animation_name)
    xp_price = animation_data.get("xp_price") if animation_data else None

    if not animation_data or xp_price is None:
        return HttpResponse("❌ This animation has not yet been configured.")
    if player.xp < xp_price:
        return HttpResponse("❌ You do not have enough XP to roll this animation.")

    player.xp -= xp_price
    rolled_animation = animation.roll_animation(animation_name)
    player.signatures[animation_name] = rolled_animation
    player.save()

    return render(
        request,
        "players/fragments/animation_result_fragment.html",
        {
            "player": player,
            "rolled_animation": rolled_animation,
            "animation_name": animation_name,
        },
    )


# This function based htmx view will allow the user to generate a girlfriend for the player
def htmx_generate_girlfriend(request, id):

    # Check if the player exists & belongs to the current user
    player = get_object_or_404(Player, pk=id)
    if player.user != request.user:
        return render(request, "500.html", {"reason": "You do not own this player"})
    if player.girlfriend:
        return HttpResponse(
            "❌ You already have a spouse, please break up with them first."
        )

    # Generate a girlfriend
    girlfriend = get_girlfriend()

    # Update the player's girlfriend field (assumes JSONField or TextField)
    player.girlfriend = girlfriend
    player.save()

    description = (
        f"Meet {girlfriend['name']}, a {girlfriend['age']}-year-old who stands "
        f"{girlfriend['height']} feet tall and weighs {girlfriend['weight']} lbs. "
        f"{girlfriend['pronouns'][1].capitalize()} loves {', '.join(girlfriend['hobbies'])}, "
        f"adores the color {girlfriend['favorite_color']}, and could eat {girlfriend['favorite_food']} every day. "
        f"{girlfriend['pronouns'][1].capitalize()}'s favorite movie is '{girlfriend['favorite_movie']}', "
        f"and {girlfriend['pronouns'][0]}'s usually listening to {', '.join(girlfriend['favorite_music'])}. "
        f"People describe {girlfriend['pronouns'][1]} as {', '.join(girlfriend['personality_traits'])}."
    )

    # Optionally: send to webhook, Discord, logs, etc.
    webhook.send_webhook(
        url="tinder",
        title=f"🍆 {player.first_name} {player.last_name} has a new spouse!",
        body=description,
    )

    return HttpResponse("✅ Spouse generated successfully")
