# Python imports
import json

# Local imports
from logs.models import UpgradeLog

# A function used to return an accurate range by including the end of the range
def real_range(start, end):
    return range(start, (end + 1))


# A function used to format the height of a player
def imperial_height(inches):
    return f"{inches // 12}'{inches % 12}"


# A function used to compile every player upgrade into a single dictionary for Sync2K
def compile_player_upgrades():
    upgrades = {}
    upgrade_logs = UpgradeLog.objects.filter(complete=False).order_by("player__team")
    for log in upgrade_logs:
        # Initialize the dictionary
        full_name = f"{log.player.first_name} {log.player.last_name}"
        upgrades[full_name] = {
            "firstName": log.player.first_name,
            "lastName": log.player.last_name,
            "attributes": {},
            "badges": {},
            "tendencies": {},
        }
        # Add the attributes
        for attribute, data in log.upgrades["attributes"].items():
            upgrades[full_name]["attributes"][attribute] = data["new"]
        # Add the badges
        for badge, data in log.upgrades["badges"].items():
            upgrades[full_name]["badges"][badge] = data["new"]
        # Add the tendencies
        for tendency, data in log.upgrades["tendencies"].items():
            upgrades[full_name]["tendencies"][tendency] = data["new"]
    # Return the compiled upgrades
    return upgrades
