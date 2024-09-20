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
def get_surcharge_tier(player):
    # Returns 'None' if the player hasn't spent enough SP to reach the first tier
    surcharge_tiers = config.CONFIG_PLAYER["SURCHARGE_TIERS"]
    surcharge_tiers = dict(sorted(surcharge_tiers.items(), key=lambda item: item[0], reverse=True))
    sp_spent = player.sp_spent
    for threshold, percentage in surcharge_tiers.items():
        if sp_spent >= threshold:
            return percentage
