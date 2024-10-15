# Python imports
import random

# Local imports
from accounts.models import CustomUser
import simulation.config as config

# Max anomaly heights
max_anomaly_heights = {
    "PG": 81,
    "SG": 83,
    "SF": 85,
    "PF": 86,
}

# These are anomaly methods that are called when an anomaly is received
def height_anomaly(player):
    # Initialize the anomaly effects
    player.anomaly = True
    player.height += random.randint(1, 3)
    # Make sure height isn't over 'max_anomaly_heights' entry
    if player.position in max_anomaly_heights and player.height > max_anomaly_heights[player.position]:
        player.height = max_anomaly_heights[player.position]
    # Set the random boost values
    speed_boost = random.randint(5, 10)
    agility_boost = random.randint(5, 10)
    strength_boost = random.randint(5, 10)
    vertical_boost = random.randint(5, 10)
    # Boost the player's attributes (capped at 99)
    player.attributes["Speed"] = min(99, player.attributes["Speed"] + speed_boost)
    player.attributes["Speed with Ball"] = player.attributes["Speed"]
    player.attributes["Agility"] = min(99, player.attributes["Agility"] + agility_boost)
    player.attributes["Strength"] = min(99, player.attributes["Strength"] + strength_boost)
    player.attributes["Vertical"] = min(99, player.attributes["Vertical"] + vertical_boost)
    # Return the player (we'll need to save this later)
    return player


# Changes the chance of an anomaly occurring
# Each anomaly points to a function that applies the anomaly
anomaly_chances = 0.01
anomalies = {
    "Height": height_anomaly,
}


# Rolls for an anomaly
def anomaly_roll(player: any):
    received_anomaly = random.random() < anomaly_chances
    if received_anomaly:
        anomaly_chosen = random.choice(list(anomalies.keys()))
        anomaly_player = anomalies[anomaly_chosen](player)
        return anomaly_player
    else:
        return player
