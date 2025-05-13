# Local imports
import random

from faker import Faker

import simulation.config as config


# Function that manages a players simulation rating
class SimulationRating:
    def __init__(self, player):
        self.player = player

    def get_rating(self):
        # Calculate the simulation rating
        attribute_avg = round(
            (sum(self.player.attributes.values()) / len(self.player.attributes)), 2
        )
        badge_avg = round(
            (sum(self.player.badges.values()) / len(self.player.badges)), 2
        )
        rating = round(
            (attribute_avg)
            + (badge_avg * 1.5)
            + (self.player.sp_spent / 1000)
            + (self.player.xp_spent / 2000),
            2,
        )
        return rating


# Function that returns the surcharge tier/percentage for a player for dynamic pricing
def get_sp_surcharge(new_sp_spent):
    # Define the surcharge interest variables
    surcharge_threshold = config.CONFIG_PLAYER["SURCHARGE_THRESHOLD"]  # 1000 SP
    surcharge_step = config.CONFIG_PLAYER["SURCHARGE_STEP"]  # 500 SP
    surcharge_interest = config.CONFIG_PLAYER["SURCHARGE_DEFAULT_INTEREST"]  # 0.05 (5%)
    surcharge_interest_step = config.CONFIG_PLAYER[
        "SURCHARGE_INTEREST_INCREMENT"
    ]  # 0.01 (1%)
    surcharge_steps = round(new_sp_spent / surcharge_step)
    # Check if the player has spent enough SP to reach the kick-in threshold
    if new_sp_spent < surcharge_threshold:
        return 0
    # Calculate the number of steps above the threshold
    surcharge_steps = (
        new_sp_spent - surcharge_threshold
    ) // surcharge_step  # Calculate the number of steps above the threshold
    total_interest = surcharge_interest + (
        surcharge_steps * surcharge_interest_step
    )  # Add base interest to (steps above threshold * interest step)
    # Return the surcharge interest (rounded to 2 decimal places)
    return round(total_interest, 2)


# Function that returns a random girlfriend object
def get_girlfriend():
    fake = Faker()
    make_gay = random.choice([True, False])
    pronouns = ["she", "her"] if not make_gay else ["he", "him"]

    hobbies_pool = [
        "reading",
        "shopping",
        "traveling",
        "cooking",
        "dancing",
        "painting",
        "yoga",
        "gardening",
        "baking",
        "hiking",
        "photography",
        "swimming",
        "video games",
        "scrapbooking",
        "volunteering",
        "writing poetry",
        "watching documentaries",
        "collecting vinyl",
        "playing instruments",
        "cycling",
        "calligraphy",
        "climbing",
    ]

    food_pool = [
        "sushi",
        "pizza",
        "pasta",
        "tacos",
        "ramen",
        "steak",
        "salad",
        "curry",
        "pho",
        "falafel",
        "dim sum",
        "burger",
        "lasagna",
        "pad thai",
        "fried chicken",
        "gyros",
        "quesadillas",
        "poke bowls",
        "gnocchi",
        "burritos",
        "shakshuka",
        "bibimbap",
    ]

    music_pool = [
        "pop",
        "rock",
        "jazz",
        "classical",
        "hip-hop",
        "country",
        "electronic",
        "indie",
        "blues",
        "reggae",
        "folk",
        "K-pop",
        "metal",
        "lofi",
        "EDM",
        "punk",
        "gospel",
        "ambient",
        "techno",
        "drum and bass",
        "funk",
    ]

    traits_pool = [
        "funny",
        "caring",
        "adventurous",
        "loyal",
        "ambitious",
        "independent",
        "creative",
        "thoughtful",
        "spontaneous",
        "kind",
        "honest",
        "patient",
        "curious",
        "intelligent",
        "compassionate",
        "witty",
        "empathetic",
        "brave",
        "playful",
        "generous",
        "outgoing",
        "calm",
    ]

    girlfriend = {
        "name": fake.name_female() if not make_gay else fake.name_male(),
        "pronouns": pronouns,
        "age": random.randint(18, 35),
        "height": round(random.uniform(4.9, 6.0), 1),  # in feet
        "weight": random.randint(100, 160),  # in pounds
        "hobbies": random.sample(hobbies_pool, k=3),
        "favorite_color": fake.color_name(),
        "favorite_food": random.choice(food_pool),
        "favorite_movie": fake.catch_phrase(),
        "favorite_music": random.sample(music_pool, k=2),
        "personality_traits": random.sample(traits_pool, k=3),
    }

    return girlfriend
