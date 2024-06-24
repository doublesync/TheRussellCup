# Python imports
import random

# Local imports
from accounts.models import CustomUser
import simulation.config as config


# These are anomaly methods that are called when an anomaly is received
def height_anomaly(player):
    # Initialize the anomaly effects
    player.anomaly = True
    player.height += random.randint(1, 3)
    player.user.sp += config.CONFIG_PLAYER["SP_ANOMALY_BONUS"]
    # Set the random boost values
    speed_boost = random.randint(5, 10)
    acceleration_boost = random.randint(5, 10)
    strength_boost = random.randint(5, 10)
    vertical_boost = random.randint(5, 10)
    # Boost the player's attributes (capped at 99)
    player.attributes["Speed"] = min(99, player.attributes["Speed"] + speed_boost)
    player.attributes["Speed with Ball"] = player.attributes["Speed"]
    player.attributes["Acceleration"] = min(99, player.attributes["Acceleration"] + acceleration_boost)
    player.attributes["Strength"] = min(99, player.attributes["Strength"] + strength_boost)
    player.attributes["Vertical"] = min(99, player.attributes["Vertical"] + vertical_boost)
    # Save the player
    return player


# Changes the chance of an anomaly occurring
# Each anomaly points to a function that applies the anomaly
anomaly_chances = 0.50
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
