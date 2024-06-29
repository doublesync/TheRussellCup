# Python imports

# Django imports
from django.http import HttpResponse
from django.shortcuts import render

# Local imports
from teams.models import Team, Draft, DraftPick, DraftOrder

# Create your views here.
def team_page(request, id):
    team = Team.objects.get(pk=id)
    return render(request, "teams/team_page.html", {"team": team})

def team_list(request):
    teams = Team.objects.all()
    return render(request, "teams/team_list.html", {"teams": teams})

def draft_page(request, id):
    draft = Draft.objects.get(pk=id)
    draft_order = DraftOrder.objects.filter(draft=draft).order_by("order")
    return render(request, "teams/draft_page.html", {"draft": draft, "draft_order": draft_order})

def draft_list(request):
    return HttpResponse("Work in progress...")