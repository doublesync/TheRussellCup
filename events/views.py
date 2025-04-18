from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import View

from events.models import Entree, Event
from players.models import Player


def events_list(request):
    """
    A function that displays a list of events.
    """

    return render(request, "events/events_list.html", {"events": Event.objects.all()})


def view_event(request, event_id):
    """
    A function that displays the details of an event.
    """

    return render(
        request,
        "events/view_event.html",
        {
            "event": Event.objects.get(id=event_id),
            "entries": Entree.objects.filter(event=event_id).order_by(
                "-player__sp_spent"
            ),
            "entry_count": Entree.objects.filter(event=event_id).count(),
            "players": Player.objects.filter(user=request.user),
        },
    )


class AddEntryView(View):
    """
    A class-based view that handles adding a player to an event.
    """

    def post(self, request, *args, **kwargs):
        """
        Handles the POST request to add a player to an event.
        """

        player, event = self.get_player_and_event(request)

        error = self.validate_entry(player, event)
        if error:
            return HttpResponse(error)

        self.create_entry(player, event)
        return HttpResponse("✅ Player added to event successfully!")

    def get_player_and_event(self, request):
        """
        Retrieves the player and event from the request.
        """

        player_id = request.POST.get("id")
        event_id = request.POST.get("event_id")

        player = get_object_or_404(Player, id=player_id)
        event = get_object_or_404(Event, id=event_id)

        return player, event

    def validate_entry(self, player, event):
        """
        Validates if a player can be added to an event.
        """

        if Entree.objects.filter(player=player, event=event).exists():
            return "❌ You have already entered that event."

        if Entree.objects.filter(event=event).count() >= event.max_entries:
            return "❌ That event is full."

        is_free_agent = not player.team
        is_active_player = bool(player.team)

        if not event.rookies_allowed and player.rookie:
            return "❌ That event does not allow rookies."

        if not event.free_agents_allowed and is_free_agent:
            return "❌ That event does not allow free agents."

        if not event.active_players_allowed and is_active_player:
            return "❌ That event does not allow active players."

        if event.use_spent_limit and player.sp_spent > event.spent_limit:
            return f"❌ That event does not allow players who have spent more than ${event.spent_limit}."

        return None

    def create_entry(self, player, event):
        """
        Creates an entry for a player in an event.
        """

        Entree.objects.create(player=player, event=event)
