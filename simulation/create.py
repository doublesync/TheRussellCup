# Python imports

# Local imports
import simulation.scripts.default as default


# Class that holds methods that take us through the player creation process
class CreatePlayer:
    def __init__(self, first_name, last_name, position, number, user):
        # User defined fields
        self.first_name = first_name
        self.last_name = last_name
        self.position = position
        self.number = number
        self.user = user
        # Server defined fields
        self.attributes = default.default_attributes()
        self.badges = default.default_badges()
        # Randomly generated fields
        self.height = None
        self.weight = None
        self.wingspan = None
        self.jumpshot = None
        self.anomaly = False
