# Python imports
import random

# Local imports
from simulation.scripts.utility import real_range

# Default height and wingspan odds used for skilled and athletic players
height_odds = {
    "PG": {
        real_range(1, 4): 72,
        real_range(5, 30): 73,
        real_range(31, 70): 74,
        real_range(71, 95): 75,
        real_range(96, 100): 76,
    },
    "SG": {
        real_range(1, 4): 74,
        real_range(5, 30): 75,
        real_range(31, 71): 76,
        real_range(72, 96): 77,
        real_range(97, 100): 78,
    },
    "SF": {
        real_range(1, 3): 76,
        real_range(4, 28): 77,
        real_range(29, 70): 78,
        real_range(71, 95): 79,
        real_range(96, 100): 80,
    },
    "PF": {
        real_range(1, 3): 78,
        real_range(4, 28): 79,
        real_range(29, 70): 80,
        real_range(71, 95): 81,
        real_range(96, 100): 82,
    },
    "C": {
        real_range(1, 4): 80,
        real_range(5, 28): 81,
        real_range(29, 70): 82,
        real_range(71, 95): 83,
        real_range(96, 100): 84,
    },
}


# Roll for the players height
def height_roll(position):
    roll = random.randint(1, 100)
    for key, value in height_odds[position].items():
        if roll in key:
            return value
