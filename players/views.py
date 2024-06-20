# Python imports

# Django imports
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic.edit import FormView

# Local imports
from players.forms import PlayerForm
import simulation.create as create

# Create your views here.


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
            return JsonResponse({"status": "success"})
