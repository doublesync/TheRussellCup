# Django imports
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Local imports
from accounts.models import CustomUser
from players.models import Player


@login_required
def home(request):
    # Flat gives back single values: ('a', 'b', 'c') instead of tuples: [('a',), ('b',), ('c',)]
    care_package_users = CustomUser.objects.filter(has_care_package=True).values_list("username", flat=True)
    user_players = Player.objects.filter(user=request.user)
    return render(request, "pages/home.html", {"player_files": user_players, "care_package_users": care_package_users})

def google_adsense(request):
    return HttpResponse("google.com, pub-4085265783135188, DIRECT, f08c47fec0942fa0")