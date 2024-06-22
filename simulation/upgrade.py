# Python imports


# Local imports


# An example of data that will be passed to the upgrade creator
example_data = {
    "attributes": [
        # [0] is the attribute name, [1] is the attribute value
        ["Driving Dunk", 10],
        ["Standing Dunk", 10],
        ["Three Point Shot", 10],
        ["Mid Range Shot", 10],
    ],
    "badges": [
        # [0] is the badge name, [1] is the badge level
        ["Slithery Finisher", 2],
        ["Catch and Shoot", 2],
        ["Clamps", 3],
        ["Quick Draw", 4],
    ],
}


# Class that holds methods that take us through the upgrade process
class UpgradeCreator:
    def __init__(self, user, player, data):
        self.player = player
        self.user = user
        self.data = data

    def format(self):
        pass

    def calculate(self):
        pass

    def validate(self):
        pass

    def purchase(self):
        pass
