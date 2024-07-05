# Django imports
from django.db import models
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views import View

# Local imports
import simulation.config as config
import simulation.scripts.attribute as attribute
import simulation.scripts.badge as badge
import simulation.scripts.tendency as tendency
from logs.models import UpgradeLog, PaymentLog
from players.models import Player

# A function based view that will be used to display all of the logs
def view_logs(request, id):
    player = get_object_or_404(Player, id=id)
    current_week = config.CONFIG_SEASON["CURRENT_WEEK"]
    current_season = config.CONFIG_SEASON["CURRENT_SEASON"]
    upgrade_logs = UpgradeLog.objects.filter(player=player, week=current_week, season=current_season)
    payment_logs = PaymentLog.objects.filter(player=player, week=current_week, season=current_season, type="SP")
    payment_sum_week = payment_logs.aggregate(models.Sum("payment"))["payment__sum"]
    return render(request, template_name="logs/view_logs.html", context={
        "player": player, 
        "upgrade_logs": upgrade_logs, 
        "payment_logs": payment_logs, 
        "payment_data": {
            "current_week": current_week,
            "current_season": current_season,
            "payment_sum_week": payment_sum_week,
            "max_sp_week": config.CONFIG_SEASON["MAX_SP_WEEK"],
            "max_sp_season": config.CONFIG_SEASON["MAX_SP_SEASON"],
        }
    })

# A function based view that will be used to display the upgrade log
def upgrade_log(request, id):
    # Get the upgrade log
    log = UpgradeLog.objects.get(id=id)
    # Get the categories for the attributes, badges, and tendencies
    attribute_categories = attribute.attribute_categories
    badge_categories = badge.badge_categories
    tendency_categories = tendency.tendency_categories
    # Let's order the attributes, badges, and tendencies by their categories
    log.upgrades["attributes"] = {category: {attribute: log.upgrades["attributes"][attribute] for attribute in log.upgrades["attributes"] if attribute in attribute_categories[category]} for category in attribute_categories}
    log.upgrades["badges"] = {category: {badge: log.upgrades["badges"][badge] for badge in log.upgrades["badges"] if badge in badge_categories[category]} for category in badge_categories}
    log.upgrades["tendencies"] = {category: {tendency: log.upgrades["tendencies"][tendency] for tendency in log.upgrades["tendencies"] if tendency in tendency_categories[category]} for category in tendency_categories}
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
        return render(request, template_name="logs/incomplete_logs.html", context={"upgrade_logs": upgrade_logs})
    
# A function based view that will mark an upgrade as complete
def mark_upgrade_complete(request, id):
    if request.method == "POST":
        # Check if the user has permission to mark upgrades as complete
        if request.user.can_mark_upgrades:
            log = UpgradeLog.objects.get(id=id)
            log.complete = True
            log.save()
            return HttpResponse("✅ Upgrade marked as complete.")
