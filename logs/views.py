# Python imports
import json

# Django imports
from django.db import models
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views import View
from django.utils import timezone as tz

# Local imports
import simulation.webhook as webhook
import simulation.config as config
import simulation.scripts.attribute as attribute
import simulation.scripts.badge as badge
import simulation.scripts.tendency as tendency
from logs.models import UpgradeLog, PaymentLog
from players.models import Player
from simulation.scripts.utility import compile_player_upgrades

# A function based view that will be used to display all of the logs
def view_logs(request, id):
    player = get_object_or_404(Player, id=id)
    current_week = config.CONFIG_SEASON["CURRENT_WEEK"]
    current_season = config.CONFIG_SEASON["CURRENT_SEASON"]
    upgrade_logs = UpgradeLog.objects.filter(player=player, week=current_week, season=current_season)
    payment_logs = PaymentLog.objects.filter(player=player, season=current_season, type="SP").order_by("-created")
    payment_sum_season = payment_logs.aggregate(models.Sum("payment"))["payment__sum"]
    return render(request, template_name="logs/view_logs.html", context={
        "player": player, 
        "upgrade_logs": upgrade_logs, 
        "payment_logs": payment_logs, 
        "payment_data": {
            "current_week": current_week,
            "current_season": current_season,
            "payment_sum_season": payment_sum_season,
            "max_sp_season": config.CONFIG_SEASON["MAX_SP_SEASON"],
        }
    })

# A function based view that will be used to display the upgrade log
def upgrade_log(request, id):
    # Get the upgrade log
    log = UpgradeLog.objects.get(id=id)
    # Let's order the attributes, badges, and tendencies by their categories
    log.upgrades["attributes"] = attribute.order_attributes(log.upgrades["attributes"])
    log.upgrades["badges"] = badge.order_badges(log.upgrades["badges"])
    log.upgrades["tendencies"] = tendency.order_tendencies(log.upgrades["tendencies"])
    # Render the upgrade log
    return render(request, template_name="logs/upgrade_log.html", context={"log": log})
    
# A function based view that will be used to display the payment log
def payment_log(request, id):
    log = PaymentLog.objects.get(id=id)
    return render(request, template_name="logs/payment_log.html", context={"log": log})

# A class based view that will list all of the logs that aren't completed
class IncompleteLogs(View):
    def get(self, request):
        # Check if the user has permission to view this page
        if not request.user.can_mark_upgrades:
            return render(request, template_name="500.html", context={"reason": "You do not have permission to view this page."})
        # Get all of the logs that aren't completed
        upgrade_logs = UpgradeLog.objects.filter(complete=False).order_by("player__team")
        compiled_upgrades = compile_player_upgrades() # for Sync2K
        # Create a file object that can be downloaded in the template

        # Render the template
        return render(request, template_name="logs/incomplete_logs.html", context={"upgrade_logs": upgrade_logs})
    
# A function based view that will mark an upgrade as complete
def mark_upgrade_complete(request, id):
    if request.method == "POST":
        # Check if the user has permission to mark upgrades as complete
        if request.user.can_mark_upgrades:
            # Create the upgrade log
            log = UpgradeLog.objects.get(id=id)
            log.complete = True
            log.save()
            # Create a discord webhook
            webhook.send_webhook(
                url="marked_upgrades",
                title=f"✅ Updated completed by {request.user.username}",
                body=f"# Update Details\n## Player\n ### {log.player}\n### Upgrades ```{log.upgrades}```",
            )
            # Return a response
            return HttpResponse("✅ Upgrade marked as complete.")
        

# A function based view that will download the incomplete logs
def download_incomplete_logs(request):
    compiled_upgrades = compile_player_upgrades()
    json_data = json.dumps(compiled_upgrades, indent=4)  # Beautify for readability
    response = HttpResponse(json_data, content_type='application/json')
    # Get the date of today separated by dashes (month and day)
    now = tz.now().strftime("%H%M%S")
    response['Content-Disposition'] = f'attachment; filename="{now}.json"'
    return response

def google_adsense(request):
    return HttpResponse("google.com, pub-4085265783135188, DIRECT, f08c47fec0942fa0")