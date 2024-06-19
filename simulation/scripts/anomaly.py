# Python imports
import random

# Local imports
from accounts.models import CustomUser
import simulation.config as config


# These are anomaly methods that are called when an anomaly is received
def height_anomaly(player):
    player.height += 3
    player.anomaly = True
    player.user.sp += config["CONFIG_PLAYER"]["SP_ANOMALY_BONUS"]
    return player


# Changes the chance of an anomaly occurring
# Each anomaly points to a function that applies the anomaly
anomaly_chances = 0.02
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
