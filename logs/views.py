import json

from django.contrib import messages
from django.db import models
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

import simulation.config as config
import simulation.scripts.attribute as attribute
import simulation.scripts.badge as badge
import simulation.scripts.tendency as tendency
import simulation.webhook as webhook
from logs.models import PaymentLog, UpgradeLog
from players.models import Player
from simulation.scripts.utility import compile_player_upgrades


def view_logs(request, log_id):
    """
    A function based view that will be used to display the logs of a player
    """

    player = get_object_or_404(Player, id=log_id)
    current_week = config.CONFIG_SEASON["CURRENT_WEEK"]
    current_season = config.CONFIG_SEASON["CURRENT_SEASON"]
    upgrade_logs = UpgradeLog.objects.filter(
        player=player, week=current_week, season=current_season
    )
    payment_logs = PaymentLog.objects.filter(
        player=player, season=current_season, type="SP"
    ).order_by("-created")
    payment_sum_season = payment_logs.aggregate(models.Sum("payment"))["payment__sum"]

    return render(
        request,
        "logs/view_logs.html",
        {
            "player": player,
            "upgrade_logs": upgrade_logs,
            "payment_logs": payment_logs,
            "payment_data": {
                "current_week": current_week,
                "current_season": current_season,
                "payment_sum_season": payment_sum_season,
                "max_sp_season": config.CONFIG_SEASON["MAX_SP_SEASON"],
            },
        },
    )


def upgrade_log(request, log_id):
    """
    A function based view that will be used to display the upgrade log of a player
    """

    log = UpgradeLog.objects.get(id=log_id)
    log.upgrades["attributes"] = attribute.order_attributes(log.upgrades["attributes"])
    log.upgrades["badges"] = badge.order_badges(log.upgrades["badges"])
    log.upgrades["tendencies"] = tendency.order_tendencies(log.upgrades["tendencies"])

    return render(request, "logs/upgrade_log.html", {"log": log})


def payment_log(request, log_id):
    """
    A function based view that will be used to display the payment log of a player
    """

    log = PaymentLog.objects.get(id=log_id)

    return render(request, "logs/payment_log.html", {"log": log})


class IncompleteLogs(View):
    """
    A class based view that will be used to display the incomplete logs of a player
    """

    def get(self, request):
        """
        A method that will be used to display the incomplete logs of a player
        """

        if not request.user.can_mark_upgrades:
            return render(
                request,
                "500.html",
                {"reason": "You do not have permission to view this page."},
            )

        upgrade_logs = UpgradeLog.objects.filter(complete=False).order_by(
            "player__team"
        )
        compiled_upgrades = compile_player_upgrades()  # for Sync

        return render(
            request,
            "logs/incomplete_logs.html",
            {"upgrade_logs": upgrade_logs},
        )


def mark_upgrade_complete(request, log_id):
    """
    A function based view that will be used to mark an upgrade as complete
    """

    if request.method == "POST":
        if request.user.can_mark_upgrades:
            log = UpgradeLog.objects.get(id=log_id)
            log.complete = True
            log.save()

            webhook.send_webhook(
                url="marked_upgrades",
                title=f"✅ Updated completed by {request.user.username}",
                body=f"# Update Details\n## Player\n ### {log.player}\n### Upgrades ```{log.upgrades}```",
            )

            return HttpResponse("✅ Upgrade marked as complete.")


def download_incomplete_logs(request):
    """
    A function based view that will be used to download the incomplete logs of a player
    """

    compiled_upgrades = compile_player_upgrades()
    json_data = json.dumps(compiled_upgrades, indent=4)
    response = HttpResponse(json_data, content_type="application/json")
    response["Content-Disposition"] = 'attachment; filename="export.json"'

    return response


def mark_all_upgrades_complete(request):
    """
    A function based view that will be used to mark all upgrades as complete
    """

    if request.user.can_mark_upgrades:
        upgrade_logs = UpgradeLog.objects.filter(complete=False)
        for log in upgrade_logs:
            log.complete = True
            log.save()

        upgrade_count = len(upgrade_logs)
        webhook.send_webhook(
            url="marked_upgrades",
            title=f"✅ Updated completed by {request.user.username}",
            body=f"# Update Details\n## Amount of Upgrades\n ### {upgrade_count}",
        )

        messages.success(request, "✔ All upgrades have been marked as complete.")
        return redirect("incomplete_logs")


def google_adsense(request):
    """
    A function based view that will be used to display the google adsense code
    """

    return HttpResponse("google.com, pub-4085265783135188, DIRECT, f08c47fec0942fa0")
