# Python imports
import json

# Django imports
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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
from players.models import Player
from players.forms import PlayerForm, UpgradeForm
import simulation.create as create
import simulation.upgrade as upgrade
import simulation.webhook as webhook
import simulation.scripts.attribute as attribute
import simulation.scripts.badge as badge


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
    player = get_object_or_404(Player, id=id)
    sorted_attributes = dict(sorted(player.attributes.items(), key=lambda x: x[1], reverse=True))
    sorted_badges = dict(sorted(player.badges.items(), key=lambda x: x[1], reverse=True))
    return render(request, "players/player_page.html", {
        "player": player, 
        "attributes": sorted_attributes, 
        "badges": sorted_badges,
        "attribute_categories": attribute.attribute_categories,
        "badge_categories": badge.badge_categories
    })
    # fmt:on


# This is a class based view that will render the form to upgrade a player
class UpgradeFormView(FormView):

    # fmt: off

    template_name = "players/upgrade_player.html"
    form_class = UpgradeForm

    def get(self, request, *args, **kwargs):
        player_id = self.kwargs.get("id")
        player = get_object_or_404(Player, id=player_id)
        if player.user != request.user:
            return render(request, "500.html", {"reason": "You do not own this player"})
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        player_id = self.kwargs.get("id")
        player = get_object_or_404(Player, id=player_id)
        sorted_attributes = dict(sorted(player.attributes.items(), key=lambda x: x[1], reverse=True))
        sorted_badges = dict(sorted(player.badges.items(), key=lambda x: x[1], reverse=True))
        context.update(
            {
                "player": player,
                "form": UpgradeForm(player=player),
                "attributes": sorted_attributes,
                "badges": sorted_badges,
                "attribute_categories": attribute.attribute_categories,
                "badge_categories": badge.badge_categories,
            }
        )
        return context

    def form_valid(self, form):
        # Initialize some objects
        player = get_object_or_404(Player, id=form.data["player_id"])
        upg = upgrade.UpgradeCreator(user=self.request.user, player=player, data=form.data)
        # If the user updated their cart (we send an HX request)
        if self.request.headers.get("HX-Request") == "true":
            cart = upg.validate_price(validate=False)[1]
            html = render_to_string("players/fragments/cart_fragment.html", {"cart": cart})
            return HttpResponse(html)
        # If the user submitted the form (we send a POST request without HX)
        else:
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
        return Player.objects.filter(user=self.request.user).order_by("-sim_rating")