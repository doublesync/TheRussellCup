# Django imports
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Local imports
from accounts.models import CustomUser
from players.models import Player


@login_required
def home(request):
    user_players = Player.objects.filter(user=request.user)
    return render(request, "pages/home.html", {"player_files": user_players})
