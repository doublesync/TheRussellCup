# Python imports

# Django imports
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View


# Local imports
from teams.models import Team, Draft, DraftPick, DraftOrder
import simulation.payment as payment
import simulation.statfinder as statfinder
import simulation.config as config

# Create your views here.
def team_page(request, id):
    # Initialize variables
    team = Team.objects.get(pk=id)
    salary_book = payment.get_salary_book(team)
    current_week = config.CONFIG_SEASON["CURRENT_WEEK"]
    # Get the players' averages & totals
    stat_finder = statfinder.StatFinder()
    team_stats = stat_finder.team_player_stats(team)
    # Loop through the players
    return render(request, "teams/team_page.html", {"team": team, "current_week": current_week, "salary_book": salary_book, "team_stats": team_stats})

def team_list(request):
    teams = Team.objects.all()
    return render(request, "teams/team_list.html", {"teams": teams})

def draft_page(request, id):
    draft = Draft.objects.get(pk=id)
    draft_order = DraftOrder.objects.filter(draft=draft).order_by("order")
    return render(request, "teams/draft_page.html", {"draft": draft, "draft_order": draft_order})

def draft_list(request):
    return HttpResponse("Work in progress...")

class RosterMoveView(View):

    def get(self, request, id):
        team = Team.objects.get(pk=id)
        if team.manager == request.user:
            return render(request, "teams/roster_move.html")

    def post(self, request):
        return HttpResponse("POST request")