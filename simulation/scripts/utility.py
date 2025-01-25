# Python imports
import json

# Local imports
from logs.models import UpgradeLog

# Physical attributes that don't change
physical_attributes = [
    "Speed",
    "Agility",
    "Vertical",
    "Strength",  
    "Speed with Ball",
]

# A function used to return an accurate range by including the end of the range
def real_range(start, end):
    return range(start, (end + 1))


# A function used to format the height of a player
def imperial_height(inches):
    return f"{inches // 12}'{inches % 12}"


# A function used to copmile a single player into a ditionary for Sync2K
def generate_player_file(player):
    # Initialize the upgrades we'll return.
    player_file = {
        "attributes": {},
        "badges": {},
        "tendencies": {}
    }
    # Don't add the item if it's in the banned list
    banned_items = ["Touches"]
    # Add attributes to the player file
    for attribute in player.attributes:
        if attribute not in banned_items:
            player_file["attributes"][attribute] = player.attributes[attribute]
    # Add badges to the player file
    for badge in player.badges:
        player_file["badges"][badge] = player.badges[badge]
    # Add tendencies to the player file
    for tendency in player.tendencies:
        player_file["tendencies"][tendency] = player.tendencies[tendency]
    # Add first and last name identifiers
    player_file["firstName"] = player.first_name
    player_file["lastName"] = player.last_name
    return player_file

# A function used to compile every player upgrade into a single dictionary for Sync2K
def compile_player_upgrades():
    upgrades = {}
    upgrade_logs = UpgradeLog.objects.filter(complete=False)
    for log in upgrade_logs:
        # Fetch the player from the log (each player has a relative player)
        player = log.player
        # Get the upgrades we'll return
        upgrades[player.id] = generate_player_file(player)
    # Return the compiled upgrades
    return upgrades