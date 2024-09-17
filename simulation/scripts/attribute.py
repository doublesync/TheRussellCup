# Local imports
from simulation.scripts.utility import real_range

# Physical attributes that don't change
physical_attributes = [
    "Speed",  # Set based on height
    "Agility",  # Set based on speed
    "Vertical",  # Set based on height
    "Strength",  # Randomly generated based on weight
    "Speed with Ball",  # Set based on height
]

# Attribute categories
attribute_categories = {
    "Offense": [
        "Driving Layup",
        "Post Fade",
        "Post Hook",
        "Post Moves",
        "Draw Foul",
        "Close Shot",
        "Midrange Shot",
        "3pt Shot",
        "Free Throw",
        "Ball Control",
        "Passing IQ",
        "Pass Accuracy",
        "Offensive Rebound",
        "Standing Dunk",
        "Driving Dunk",
        "Shot IQ",
        "Passing Vision",
        "Hands",
    ],
    "Defense": [
        "Defensive Rebound",
        "Interior Defense",
        "Perimeter Defense",
        "Block",
        "Steal",
        "Hustle", 
    ],
    "Mental": [
        "Pass Perception",
        "Defensive Consistency",
        "Help Defense IQ",
        "Offensive Consistency",
    ],
    "Physical": physical_attributes,
}

# Attribute prices (in SP)
attribute_prices = {
    real_range(55, 60): 1,
    real_range(60, 65): 2,
    real_range(66, 70): 4,
    real_range(71, 75): 5,
    real_range(76, 80): 10,
    real_range(81, 85): 20,
    real_range(86, 90): 25,
    real_range(91, 94): 30,
    real_range(95, 99): 40,
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

def order_attributes(attributes):
    # Order the attributes by their categories
    ordered_attributes = {}
    for category in attribute_categories:
        ordered_attributes[category] = {}
        for attribute in attribute_categories[category]:
            if attribute in attributes:
                ordered_attributes[category][attribute] = attributes[attribute]
    return ordered_attributes