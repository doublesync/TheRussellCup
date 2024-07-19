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