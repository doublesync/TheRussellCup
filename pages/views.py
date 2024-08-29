# Django imports
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Local imports
from accounts.models import CustomUser
from players.models import Player


@login_required
def home(request):
    user_players = Player.objects.filter(user=request.user)
    return render(request, "pages/home.html", {"player_files": user_players})

def google_adsense(request):
    return HttpResponse("google.com, pub-4085265783135188, DIRECT, f08c47fec0942fa0")