# Python imports

# Local imports
import simulation.scripts.attribute as attribute
import simulation.scripts.badge as badge
from logs.models import UpgradeLog

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


# fmt: off

# Class that holds methods that take us through the upgrade process
class UpgradeCreator:
    def __init__(self, user, player, data):
        self.player = player
        self.user = user
        self.data = data
        self.cart = {
            "total": 0,
            "attributes": {},
            "badges": {},
        }

    # Remove attributes and badges that are the same as the players
    def format(self):
        for a, value in self.data.items():
            if not a in self.player.attributes: continue
            if int(value) > self.player.attributes[a]:
                self.cart["attributes"][a] = {}
                self.cart["attributes"][a]["start"] = self.player.attributes[a]
                self.cart["attributes"][a]["new"] = int(value)
        for b, value in self.data.items():
            if not b in self.player.badges: continue
            if int(value) > self.player.badges[b]:
                self.cart["badges"][b] = {}
                self.cart["badges"][b]["start"] = self.player.badges[b]
                self.cart["badges"][b]["new"] = int(value)

    def validate_user(self):
        # Check if the user owns the player
        if self.player.user != self.user:
            return [False, "You do not own this player."]
        # Return a success message
        return [True, self.user]

    def validate_price(self, validate=True):
        # Format the data
        self.format()
        # Add the price of each attribute and badge to their cart objects (dictionaries)
        for a in self.cart["attributes"]:
            start_value = self.cart["attributes"][a]["start"]
            new_value = self.cart["attributes"][a]["new"]
            price = attribute.check_attribute_price(start_value, new_value)
            self.cart["attributes"][a]["price"] = price
            self.cart["total"] += price
        for b in self.cart["badges"]:
            start_value = self.cart["badges"][b]["start"]
            new_value = self.cart["badges"][b]["new"]
            price = badge.check_badge_price(start_value, new_value)
            self.cart["badges"][b]["price"] = price
            self.cart["total"] += price
        # Check if user can afford the upgrades
        if validate:
            if self.user.sp < self.cart["total"]:
                return [False, "You do not have enough SP to afford these upgrades."]
        # Return a success message
        return [True, self.cart]

    def validate_upgrades(self):
        # Validate attribute upgrades
        for a, data in self.cart["attributes"].items():
            if a in attribute.physical_attributes or a == "Intangibles":
                return [False, "You cannot upgrade physical attributes or Intangibles."]
            if data["new"] > 99:
                return [False, "You cannot upgrade an attribute above 99."]
        # Validate badge upgrades
        for b, data in self.cart["badges"].items():
            if data["new"] > 4:
                return [False, f"You cannot upgrade {b} above HOF."]
        # Return a success message
        return [True, self.cart]

    def purchase(self):
        # Format the data
        self.format()
        # Validate the user, price, and upgrades
        validate_user = self.validate_user()
        validate_price = self.validate_price()
        validate_upgrades = self.validate_upgrades()
        if validate_price[0] and validate_upgrades[0] and validate_user[0]:
            # Apply the price to the user
            self.user.sp -= self.cart["total"]
            self.user.save()
            # Apply the upgrades & spent to the player
            for a, data in self.cart["attributes"].items():
                self.player.attributes[a] = data["new"]
            for b, data in self.cart["badges"].items():
                self.player.badges[b] = data["new"]
            self.player.sp_spent += self.cart["total"]
            self.player.save()
            # Log the upgrades
            UpgradeLog.objects.create(player=self.player, total=self.cart["total"], upgrades=self.cart)
            # Return a success message
            return [True, "Upgrades applied successfully."]
        else:
            errors = []
            if not validate_user[0]: errors.append(validate_user[1])
            if not validate_price[0]: errors.append(validate_price[1])
            if not validate_upgrades[0]: errors.append(validate_upgrades[1])
            return [False, errors]

# fmt: on
