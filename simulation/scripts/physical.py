# Where physical attributes are calculated for players
import simulation.scripts.default as default
import simulation.scripts.weight as weight

# Starting physicals by height
starting_height_physicals = {
    72: {
        "Vertical": 84,
        "Speed": 94,
    },
    73: {
        "Vertical": 83,
        "Speed": 93,
    },
    74: {
        "Vertical": 82,
        "Speed": 91,
    },
    75: {
        "Vertical": 81,
        "Speed": 89,
    },
    76: {
        "Vertical": 80,
        "Speed": 87,
    },
    77: {
        "Vertical": 79,
        "Speed": 85,
    },
    78: {
        "Vertical": 78,
        "Speed": 83,
    },
    79: {
        "Vertical": 77,
        "Speed": 81,
    },
    80: {
        "Vertical": 76,
        "Speed": 79,
    },
    81: {
        "Vertical": 75,
        "Speed": 75,
    },
    82: {
        "Vertical": 74,
        "Speed": 70,
    },
    83: {
        "Vertical": 73,
        "Speed": 68,
    },
    84: {
        "Vertical": 72,
        "Speed": 65,
    },
    85: {
        "Vertical": 70,
        "Speed": 60,
    },
    86: {
        "Vertical": 68,
        "Speed": 57,
    },
    87: {
        "Vertical": 76,
        "Speed": 54,
    },
}


# Changes the starting physicals of a player based on their height
def set_starting_physicals(player: any) -> any:
    # fmt: off
    # These are the physical attributes that are set based on height
    player.attributes = default.default_attributes()
    player.attributes["Speed"] = starting_height_physicals[player.height]["Speed"]
    player.attributes["Speed with Ball"] = starting_height_physicals[player.height]["Speed"]
    player.attributes["Acceleration"] = starting_height_physicals[player.height]["Speed"]
    player.attributes["Vertical"] = starting_height_physicals[player.height]["Vertical"]
    player.attributes["Lateral Quickness"] = (player.attributes["Speed"] + player.attributes["Perimeter Defense"]) // 2 
    # These are the physical attributes that are set based on weight
    weight_roll_result = weight.weight_roll(player.position)
    player.weight = weight_roll_result["weight"]
    player.attributes["Strength"] = weight_roll_result["strength"]
    # fmt: on
    return player
