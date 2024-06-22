# Python imports
import random

# Local imports
from simulation.scripts.utility import real_range

# Default height and wingspan odds used for skilled and athletic players
height_odds = {
    "PG": {
        real_range(1, 4): 72, # 6'0
        real_range(5, 30): 73, # 6'1
        real_range(31, 70): 74, # 6'2
        real_range(71, 85): 75, # 6'3
        real_range(86, 90): 76, # 6'4
        real_range(91, 94): 77, # 6'5
        real_range(95, 96): 78, # 6'6
        real_range(97, 98): 79, # 6'7
        real_range(99, 100): 80, # 6'8
    },
    "SG": {
        real_range(1, 30): 75, # 6'3
        real_range(31, 71): 76, # 6'4
        real_range(72, 85): 77, # 6'5
        real_range(86, 90): 78, # 6'6
        real_range(91, 94): 79, # 6'7
        real_range(95, 96): 80, # 6'8
        real_range(97, 98): 81, # 6'9
        real_range(99, 100): 82, # 6'10
    },
    "SF": {
        real_range(1, 3): 77, # 6'5
        real_range(4, 28): 78, # 6'6
        real_range(29, 70): 79, # 6'7
        real_range(71, 90): 80, # 6'8
        real_range(91, 94): 81, # 6'9
        real_range(95, 96): 82, # 6'10
        real_range(97, 98): 83, # 6'11
        real_range(99, 100): 84, # 7'0
    },
    "PF": {
        real_range(1, 3): 79, # 6'7
        real_range(4, 28): 80, # 6'8
        real_range(29, 70): 81, # 6'9
        real_range(71, 90): 82, # 6'10
        real_range(91, 96): 83, # 6'11
        real_range(97, 98): 84, # 7'0
        real_range(99, 100): 85, # 7'1
    },
    "C": {
        real_range(1, 28): 81, # 6'9
        real_range(29, 70): 82, # 6'10
        real_range(71, 90): 83, # 6'11
        real_range(91, 96): 84, # 7'0
        real_range(97, 98): 85, # 7'1
        real_range(99, 100): 86, # 7'2
    },
}

# Roll for the players height
def height_roll(position):
    roll = random.randint(1, 100)
    for key, value in height_odds[position].items():
        if roll in key:
            return value
