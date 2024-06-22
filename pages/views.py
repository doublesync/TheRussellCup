# Django imports
from django.shortcuts import render

# Local imports
from accounts.models import CustomUser
from players.models import Player


def home(request):
    user_players = Player.objects.filter(user=request.user)
    return render(request, "pages/home.html", {"player_files": user_players})
