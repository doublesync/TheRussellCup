# Python imports

# Django imports
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic.edit import FormView

# Local imports
from players.models import Player
from players.forms import PlayerForm
import simulation.create as create
import simulation.scripts.attribute as attribute
import simulation.scripts.badge as badge

# Create your views here.


# This is a class based view that will render the form to create a player
class PlayerFormView(FormView):

    template_name = "players/create_player.html"
    form_class = PlayerForm
    success_url = "/"

    def form_valid(self, form):

        print(self.request.user)

        data = form.cleaned_data
        seed = create.CreatePlayer(
            first_name=data["first_name"],
            last_name=data["last_name"],
            position=data["position"],
            number=data["number"],
            country=data["country"],
            college=data["college"],
            user=self.request.user,
        )
        player = seed.create()
        if type(player) == str:
            messages.error(self.request, player)
            return render(self.request, self.template_name, {"form": form})
        else:
            return redirect(player_page, id=player.id)


# This is a function based view that will render the player page
@login_required
def player_page(request, id):
    # fmt:off
    player_exists = Player.objects.filter(id=id).exists()
    if player_exists:
        player = Player.objects.get(id=id)
        sorted_attributes = dict(sorted(player.attributes.items(), key=lambda x: x[1], reverse=True))
        sorted_badges = dict(sorted(player.badges.items(), key=lambda x: x[1], reverse=True))
        return render(request, "players/player_page.html", {
            "player": player, 
            "attributes": sorted_attributes, 
            "badges": sorted_badges,
            "attribute_categories": attribute.attribute_categories,
            "badge_categories": badge.badge_categories
        })
    else:
        return render(request, "500.html", {"reason": "Player does not exist"})
    # fmt:on
