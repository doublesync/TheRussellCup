# Local imports
from simulation.scripts.utility import real_range

# Tendency categories
tendency_categories = {
    "Jump Shooting": [
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
    "Layups & Dunks": [
        "Driving Layup Tendency",
        "Standing Dunk Tendency",
        "Driving Dunk Tendency",
        "Flashy Dunk",
        "Alley-Oop",
        "Putback Dunk",
        "Crash",
        "Spin Layup",
        "Hop Step Layup",
        "Euro Step Layup",
        "Floater",
    ],
    "Drive Setup": [
        "Triple Threat Pump Fake",
        "Triple Threat Jab Step",
        "Triple Threat Idle",
        "Triple Threat Shoot",
        "Setup With Sizeup",
        "Setup With Hesitation",
        "No Setup Dribble", 
    ],
    "Driving": [
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
    "Passing": [
        "Dish To Open Man",
        "Flashy Pass",
        "Alley Oop Pass",
    ],
    "Post Game": [
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
    "Defense": [
        "Pass Interception",
        "Take Charge",
        "On Ball Steal",
        "Contest Shot",
        "Block Shot",
        "Foul",
        "Hard Foul",
    ],
}

# A dictionary that contains the prices of tendencies
tendency_price = 5
tendency_lower_price = 5

# A function to check the price of a tendency
def check_tendency_price(start_level, end_level):
    cost = 0
    if end_level < start_level:
        cost = abs(end_level - start_level) * tendency_lower_price
    else:
        cost = abs(end_level - start_level) * tendency_price
    return cost
