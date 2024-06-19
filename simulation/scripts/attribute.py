# Local imports
from simulation.scripts.utility import real_range

# Physical attributes that don't change
physical_attributes = [
    "Speed",  # Set based on height
    "Acceleration",  # Set based on speed
    "Vertical",  # Set based on height
    "Strength",  # Randomly generated based on weight
    "Speed with Ball",  # Set based on height
    "Lateral Quickness",  # Set based on speed and perimeter defense
]

# Attribute categories
attribute_categories = {
    "Shooting": [
        "Post Fade",
        "Post Hook",
        "Post Moves",
        "Midrange Shot",
        "3pt Shot",
        "Free Throw",
        "Offensive Consistency",
    ],
    "Playmaking": [
        "Ball Control",
        "Passing IQ",
        "Pass Accuracy",
        "Shot IQ",
        "Passing Vision",
        "Hands",
    ],
    "Finishing": [
        "Draw Foul",
        "Driving Layup",
        "Close Shot",
        "Standing Dunk",
        "Driving Dunk",
    ],
    "Defensive": [
        "Offensive Rebound",
        "Defensive Rebound",
        "Interior Defense",
        "Perimeter Defense",
        "Block",
        "Steal",
        "Hustle",
        "Pass Perception",
        "Defensive Consistency",
        "Help Defense IQ",
    ],
    "Physical": physical_attributes,
}

# Attribute prices (in SP)
attribute_prices = {
    real_range(55, 60): 1,
    real_range(61, 75): 3,
    real_range(76, 85): 6,
    real_range(86, 90): 9,
    real_range(91, 95): 13,
    real_range(96, 99): 16,
}


# Checks the price of an attribute and returns the cost
def check_attribute_price(start_level, end_level):
    cost = 0
    start, end = (start_level + 1), (end_level + 1)
    for i in range(start, end):
        for price_range in attribute_prices:
            if i in price_range:
                cost += attribute_prices[price_range]
    return cost
