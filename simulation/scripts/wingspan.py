# Python imports
import random

# Local imports
from simulation.scripts.utility import real_range


# Wingspan odds for players
wingspan_odds = {
    real_range(1, 5): 40,
    real_range(6, 10): 45,
    real_range(11, 31): 50,
    real_range(32, 50): 55,
    real_range(51, 60): 60,
    real_range(61, 70): 65,
    real_range(71, 78): 70,
    real_range(79, 84): 75,
    real_range(85, 91): 80,
    real_range(92, 95): 85,
    real_range(96, 98): 90,
    real_range(99, 99): 95,
    real_range(100, 100): 100,
}


# Roll for the players wingspan
def wingspan_roll():
    roll = random.randint(1, 100)
    for key in wingspan_odds:
        if roll in key:
            wingspan = wingspan_odds[key]
            offset = random.randint(-3, 3)
            if (wingspan + offset) > 100:
                return wingspan - offset
            else:
                return wingspan + offset
