# Python imports

# Django imports
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models import Sum
from django.template.loader import render_to_string
from django.utils import timezone
from django.views import View

# Local imports
from events.models import Event
from events.models import Entree
from players.models import Player


# A function that returns a list of events
def events_list(request):
    context = {
        "events": Event.objects.all()
    }
    return render(request, "events/events_list.html", context)

# A function that returns a single event
def view_event(request, id):
    context = {
        "event": Event.objects.get(id=id),
        "entries": Entree.objects.filter(event=id).order_by("-player__sp_spent"),
        "entry_count": Entree.objects.filter(event=id).count(),
        "players": Player.objects.filter(user=request.user),
    }
    return render(request, "events/view_event.html", context)

# A function that allows a user to enter an event
def add_entry(request):
    # Gather some data
    event_id = request.POST.get("event_id")
    id = request.POST.get("id")
    player = Player.objects.get(id=id)
    event = Event.objects.get(id=event_id)
    # Check if player is already entered, event is full, or player is ineligible
    if Entree.objects.filter(player=player, event=event).exists():
        return HttpResponse("❌ You have already entered that event.")
    if Entree.objects.filter(event=event).count() >= event.max_entries:
        return HttpResponse("❌ That event is full.")
    # Check if player is a rookie, free agent, or active player
    is_free_agent = False
    is_active_player = False
    if player.team == None: 
        is_free_agent = True
    else:
        is_active_player = True
    # Return error message if player is ineligible
    if not event.rookies_allowed and player.rookie:
        return HttpResponse("❌ That event does not allow rookies.")
    if not event.free_agents_allowed and is_free_agent:
        return HttpResponse("❌ That event does not allow free agents.")
    if not event.active_players_allowed and is_active_player:
        return HttpResponse("❌ That event does not allow active players.")  
    if event.use_spent_limit and player.sp_spent > event.spent_limit:
        return HttpResponse(f"❌ That event does not allow players who have spent more than ${event.spent_limit}.")  
    # Return success message if player is eligible & add player entry to the event
    entry = Entree(
        player=player,
        event=event,
    )
    entry.save()
    # Return the response
    return HttpResponse("✅ Player added to event successfully!")