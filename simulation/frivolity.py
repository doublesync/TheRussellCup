# Local imports
import simulation.config as config

# Function that manages a players simulation rating
class SimulationRating:
    def __init__(self, player):
        self.player = player

    def get_rating(self):
        # Calculate the simulation rating
        attribute_avg = round((sum(self.player.attributes.values()) / len(self.player.attributes)), 2)
        badge_avg = round((sum(self.player.badges.values()) / len(self.player.badges)), 2)
        rating = round((attribute_avg) + (badge_avg * 1.5) + (self.player.sp_spent / 1000) + (self.player.xp_spent / 2000), 2)
        return rating
    
# Function that returns the surcharge tier/percentage for a player for dynamic pricing
def get_sp_surcharge(new_sp_spent):
    # Define the surcharge interest variables
    surcharge_threshold = config.CONFIG_PLAYER["SURCHARGE_THRESHOLD"] # 1000 SP
    surcharge_step = config.CONFIG_PLAYER["SURCHARGE_STEP"] # 500 SP
    surcharge_interest = config.CONFIG_PLAYER["SURCHARGE_DEFAULT_INTEREST"] # 0.05 (5%)
    surcharge_interest_step = config.CONFIG_PLAYER["SURCHARGE_INTEREST_INCREMENT"] # 0.01 (1%)
    surcharge_steps = round(new_sp_spent / surcharge_step)
    # Check if the player has spent enough SP to reach the kick-in threshold
    if new_sp_spent < surcharge_threshold:
        return 0
    # Calculate the number of steps above the threshold
    surcharge_steps = (new_sp_spent - surcharge_threshold) // surcharge_step # Calculate the number of steps above the threshold
    total_interest = surcharge_interest + (surcharge_steps * surcharge_interest_step) # Add base interest to (steps above threshold * interest step)
    # Return the surcharge interest (rounded to 2 decimal places)
    return round(total_interest, 2)