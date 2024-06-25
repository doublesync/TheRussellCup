# Local imports
from simulation.scripts.utility import real_range

# Tendency categories
tendency_categories = {
    "Finishing": [
        "Standing Dunk Tendency",
        "Driving Dunk Tendency",
        "Flashy Dunk",
        "Alley-Oop",
        "Putback Dunk",
        "Crash",
        "Driving Layup Tendency",
        "Spin Layup",
        "Hop Step Layup",
        "Euro Step Layup",
        "Floater",
        "Drive",
        "Spot Up Drive",
        "Off Screen Drive",
        "Drive Right",
        "Driving Crossover",
        "Driving Spin",
        "Driving Step Back",
        "Driving Half Spin",
        "Driving Double Crossover",
        "Driving Behind The Back",
        "Driving Dribble Hesitation",
        "Driving In And Out",
        "No Driving Dribble Move",
        "Attack Strong On Drive",
    ],
    "Shooting": [
        "Step Through Shot",
        "Shot Under Basket",
        "Shot Close",
        "Shot Close Left",
        "Shot Close Middle",
        "Shot Close Right",
        "Shot Mid",
        "Spot Up Shot Mid",
        "Off Screen Shot Mid",
        "Shot 3pt",
        "Spot Up Shot 3pt",
        "Off Screen Shot 3pt",
        "Contested Jumper Mid",
        "Contested Jumper 3pt",
        "Stepback Jumper Mid",
        "Stepback Jumper 3pt",
        "Spin Jumper",
        "Transition Pull Up 3pt",
        "Drive Pull Up 3pt",
        "Drive Pull Up Mid",
        "Use Glass",
    ],
    "Playmaking": [
        "Dish To Open Man",
        "Flashy Pass",
        "Alley Oop Pass",
    ],
    "Defensive": [
        "Pass Interception",
        "Take Charge",
        "On Ball Steal",
        "Contest Shot",
        "Block Shot",
        "Foul",
        "Hard Foul",
    ],
    "Isolation": [
        "Triple Threat Pump Fake",
        "Triple Threat Jab Step",
        "Triple Threat Idle",
        "Triple Threat Shoot",
        "Setup With Sizeup",
        "Setup With Hesitation",
        "No Setup Dribble", 
    ],
    "Post": [
        "Post Up",
        "Post Shimmy Shot",
        "Post Face Up",
        "Post Back Down",
        "Post Aggressive Backdown",
        "Shoot From Post",
        "Post Hook Left",
        "Post Hook Right",
        "Post Fade Left",
        "Post Fade Right",
        "Post Up And Under",
        "Post Hop Shot",
        "Post Step Back Shot",
        "Post Drive",
        "Post Spin",
        "Post Drop Step",
        "Post Hop Step",
    ],
    "Freelance": [
        "Shoot",
        "Touches",
        "Roll Vs Pop",
        "Transition Spot Up",
        "Iso Vs Elite Defender",
        "Iso Vs Good Defender",
        "Iso Vs Average Defender",
        "Iso Vs Poor Defender",
        "Play Discipline"
    ],
}

# A dictionary that contains the prices of tendencies
tendency_prices = {
    real_range(0, 100): 25,
}

# A function to check the price of a tendency
def check_tendency_price(start_level, end_level):
    cost = 0
    start, end = (start_level + 1), (end_level + 1)
    for i in range(start, end):
        for price_range in tendency_prices:
            if i in price_range:
                cost += tendency_prices[price_range]
    return cost