# Python imports
import random

# The weight is cosmetic
position_weight_ranges = {
    "PG": range(170, 211),  # Weight range
    "SG": range(180, 231),
    "SF": range(190, 251),
    "PF": range(200, 271),
    "C": range(210, 291),
}

# Strength is a random number between ranges
physical_effect_ranges = {
    "PG": range(50, 76),
    "SG": range(55, 81),
    "SF": range(65, 86),
    "PF": range(70, 91),
    "C": range(75, 100),
}


def weight_roll(position):
    weight_range = position_weight_ranges[position]
    physical_range = physical_effect_ranges[position]
    result = {
        "weight": random.randint(weight_range[0], weight_range[-1]),
        "strength": random.randint(physical_range[0], physical_range[-1]),
    }
    return result
