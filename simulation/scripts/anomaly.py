# Python imports
import random


# These are anomaly methods that are called when an anomaly is received
def height_anomaly(player):
    player.height += 3
    return player


# Changes the chance of an anomaly occurring
# Each anomaly points to a function that applies the anomaly
anomaly_chances = 0.02
anomalies = {
    "Height": height_anomaly,
}


# Rolls for an anomaly
def anomalyRoll(player: any):
    received_anomaly = random.random() < anomaly_chances
    if received_anomaly:
        anomaly_chosen = random.choice(list(anomalies.keys()))
        anomaly_player = anomalies[anomaly_chosen](player)
        anomaly_player.anomaly = anomaly_chosen
        return anomaly_player
    else:
        return player
