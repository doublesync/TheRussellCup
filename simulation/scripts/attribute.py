# Python imports
from math import ceil

# Local imports
from simulation.scripts.utility import real_range

# Surcharged attributes
surcharged_attributes = {
    # Surcharged attributes
    "3pt Shot": 0.61,
    "Interior Defense": 0.58,
    "Driving Dunk": 0.56,
    "Perimeter Defense": 0.56,
    "Driving Layup": 0.53,
    # Discounted attributes
    "Post Hook": -0.25,
    "Post Fade": -0.25,
    "Pass Perception": -0.25,
    "Hustle": -0.25,
    "Help Defense IQ": -0.25,
}

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
    real_range(60, 65): 3,
    real_range(66, 70): 5,
    real_range(71, 75): 8,
    real_range(76, 80): 15,
    real_range(81, 85): 25,
    real_range(86, 90): 30,
    real_range(91, 94): 40,
    real_range(95, 99): 55,
}

# Checks the price of an attribute and returns the cost
def check_attribute_price(attribute, start_level, end_level):
    # Get base cost of the attribute upgrade
    cost = 0
    start, end = (start_level + 1), (end_level + 1)
    for i in range(start, end):
        for price_range in attribute_prices:
            if i in price_range:
                cost += attribute_prices[price_range]
    # Get (base cost + surcharge) or (base cost - discount) for the attribute upgrade
    if attribute in surcharged_attributes:
        surcharge_percent = surcharged_attributes[attribute]
        cost = ceil(cost + (cost * surcharge_percent)) # Must round up to a whole number
    # Return the total upgrade cost
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
