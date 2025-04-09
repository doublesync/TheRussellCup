# Python imports
import random

# Local imports
from simulation.sync import shared_lists, conversion_list

# Animation options for players
# Each animation option has a cost in XP and a list of options to choose from.
animation_options = {
    "Jumpshot Base": {"xp_price": 0, "options": conversion_list["Jumpshot Base"]},
    "Release 1": {"xp_price": 0, "options": conversion_list["Release 1"]},
    "Release 2": {"xp_price": 0, "options": conversion_list["Release 2"]},
    "Release Timing": {"xp_price": 0, "options": conversion_list["Release Timing"]},
    "Free Throw": {"xp_price": 0, "options": conversion_list["Free Throw"]},
    "Go-To Shot": {"xp_price": 0, "options": conversion_list["Go-To Shot"]},
    "Dribble Pull-Up": {"xp_price": 0, "options": conversion_list["Dribble Pull-Up"]},
    "Spin Jumper": {"xp_price": 0, "options": conversion_list["Spin Jumper"]},
    "Hop Jumper": {"xp_price": 0, "options": conversion_list["Hop Jumper"]},
    "Layup Package": {"xp_price": 0, "options": conversion_list["Layup Package"]},
    "Go-To Dunk Package": {"xp_price": 0, "options": conversion_list["Go-To Dunk Package"]},
    "Dunk Package 1": {"xp_price": 0, "options": conversion_list["Dunk Package 1"]},
    "Dunk Package 2": {"xp_price": 0, "options": conversion_list["Dunk Package 2"]},
    "Dunk Package 3": {"xp_price": 0, "options": conversion_list["Dunk Package 3"]},
    "Dunk Package 4": {"xp_price": 0, "options": conversion_list["Dunk Package 4"]},
    "Dunk Package 5": {"xp_price": 0, "options": conversion_list["Dunk Package 5"]},
    "Dunk Package 6": {"xp_price": 0, "options": conversion_list["Dunk Package 6"]},
    "Dunk Package 7": {"xp_price": 0, "options": conversion_list["Dunk Package 7"]},
    "Dunk Package 8": {"xp_price": 0, "options": conversion_list["Dunk Package 8"]},
    "Dunk Package 9": {"xp_price": 0, "options": conversion_list["Dunk Package 9"]},
    "Dunk Package 10": {"xp_price": 0, "options": conversion_list["Dunk Package 10"]},
    "Dunk Package 11": {"xp_price": 0, "options": conversion_list["Dunk Package 11"]},
    "Dunk Package 12": {"xp_price": 0, "options": conversion_list["Dunk Package 12"]},
    "Dunk Package 13": {"xp_price": 0, "options": conversion_list["Dunk Package 13"]},
    "Dunk Package 14": {"xp_price": 0, "options": conversion_list["Dunk Package 14"]},
    "Dunk Package 15": {"xp_price": 0, "options": conversion_list["Dunk Package 15"]},
    "Post Fade": {"xp_price": 0, "options": conversion_list["Post Fade"]},
    "Post Hook": {"xp_price": 0, "options": conversion_list["Post Hook"]},
    "Post Hop Shot": {"xp_price": 0, "options": conversion_list["Post Hop Shot"]},
    "Post Spin Shot": {"xp_price": 0, "options": conversion_list["Post Spin Shot"]},
    "Dribble Style": {"xp_price": 0, "options": conversion_list["Dribble Style"]},
    "Pass Style": {"xp_price": 0, "options": conversion_list["Pass Style"]},
    "Signature Size-Up": {"xp_price": 0, "options": conversion_list["Signature Size-Up"]},
    "Regular Breakdown Combos": {"xp_price": 0, "options": conversion_list["Regular Breakdown Combos"]},
    "Aggressive Breakdown Combos": {"xp_price": 0, "options": conversion_list["Aggressive Breakdown Combos"]},
    "Escape Moves": {"xp_price": 0, "options": conversion_list["Escape Moves"]},
    "Crossover Combos": {"xp_price": 0, "options": conversion_list["Crossover Combos"]},
    "Moving Crossover": {"xp_price": 0, "options": conversion_list["Moving Crossover"]},
    "Moving Behind The Back": {"xp_price": 0, "options": conversion_list["Moving Behind The Back"]},
    "Moving Stepback": {"xp_price": 0, "options": conversion_list["Moving Stepback"]},
    "Moving Spin": {"xp_price": 0, "options": conversion_list["Moving Spin"]},
    "Moving Hesitation": {"xp_price": 0, "options": conversion_list["Moving Hesitation"]},
    "Triple Threat Style": {"xp_price": 0, "options": conversion_list["Triple Threat Style"]},
    "Motion Style": {"xp_price": 0, "options": conversion_list["Motion Style"]},
    "Pre-Game 1": {"xp_price": 0, "options": conversion_list["Pre-Game 1"]},
    "Pre-Game 2": {"xp_price": 0, "options": conversion_list["Pre-Game 2"]},
    "Jumpball Ritual": {"xp_price": 0, "options": conversion_list["Jumpball Ritual"]},
    "Dunk Emotion": {"xp_price": 0, "options": conversion_list["Dunk Emotion"]},
    "Chew Gum": {"xp_price": 0, "options": conversion_list["Chew Gum"]},
}

# Jumpshot list
jumpshot_list = shared_lists["Jumpshots"]
jumpshot_timing_odds = (["Very Slow"] * 5 + ["Slow"] * 10 + ["Normal"] * 75 +["Quick"] * 5 + ["Very Quick"] * 5)
free_throw_list = conversion_list["Free Throw"]

# Returns a player with randomly generated jumpshot fields
def generate_jumpshot(player):
    player.jumpshot = random.choice(jumpshot_list)
    player.jumpshot_release_1 = random.choice(jumpshot_list)
    player.jumpshot_release_2 = random.choice(jumpshot_list)
    player.jumpshot_blending = random.randint(0, 100)
    player.jumpshot_timing = random.choice(jumpshot_timing_odds)
    player.jumpshot_free_throw = random.choice(free_throw_list)
    return player