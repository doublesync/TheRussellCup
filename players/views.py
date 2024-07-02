# Python imports
from collections import namedtuple
import json
import types

# Django imports
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.views.generic.edit import FormView
from django.views.generic.base import View
from django.views.generic.list import ListView

# Local imports
from players.models import Player, Modification
from players.forms import PlayerForm, UpgradeForm
import simulation.create as create
import simulation.upgrade as upgrade
import simulation.webhook as webhook
import simulation.scripts.attribute as attribute
import simulation.scripts.badge as badge
import simulation.scripts.tendency as tendency


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
    sorted_attributes = dict(sorted(player.attributes.items(), key=lambda x: x[1], reverse=True))
    sorted_badges = dict(sorted(player.badges.items(), key=lambda x: x[1], reverse=True))
    sorted_tendencies = dict(sorted(player.tendencies.items(), key=lambda x: x[1], reverse=True))
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

    model = Player
    template_name = "players/player_list.html"
    context_object_name = "players"
    paginate_by = 20

    def get_queryset(self):
        return Player.objects.all().order_by("-sim_rating")


# This is a function based view that will render a filtered player list
def htmx_search_players(request):
    # Get the page
    page = request.GET.get("page")
    # Check search_query (if it exists)
    search_query = request.POST.get("search-query")
    if search_query:
        player_list = Player.objects.filter(Q(first_name__icontains=search_query) | Q(last_name__icontains=search_query))
    else:
        player_list = Player.objects.all()
    # Check sortQuery (if it exists)
    sort_query = request.POST.get("sort-query")
    if sort_query:
        sort_field, sort_direction = sort_query.split(":")
        player_list = player_list.order_by(
            f"{'-' if sort_direction == 'desc' else ''}{sort_field}"
        )
    # Paginate the page
    paginator = Paginator(player_list, 20)
    players = paginator.get_page(page)
    # Return the page
    context: dict = {"page_obj": players}
    html: str = render_to_string("players/fragments/list_fragment.html", context)
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
        return Modification.objects.filter(expired=False).order_by("created")
    
# This is a function based view that will allow the user to purchase a modification
def purchase_modification(request, id):
    # Get the modification
    user = request.user
    mod = Modification.objects.get(pk=id)
    player_id = request.POST.get("mod-player")
    player = Player.objects.get(pk=player_id)
    existing_mods = player.modifications
    # Validate some conditions
    if player.user != user: 
        return None
    if user.xp < mod.xp_price:
        return HttpResponse("❌ You do not have enough XP to purchase this modification")
    if existing_mods and mod.item in existing_mods:
        return HttpResponse("❌ You already own this modification")
    # Purchase the modification
    if player.modifications:
        player.modifications[mod.item] = True
    else:
        player.modifications = {mod.item: True}
    user.xp -= mod.xp_price
    player.xp_spent += mod.xp_price
    player.save()
    user.save()
    # Return a success message
    return HttpResponse("✅ Modification purchased successfully")