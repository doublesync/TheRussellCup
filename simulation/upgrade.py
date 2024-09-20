# Python imports

# Local imports
import simulation.scripts.attribute as attribute
import simulation.scripts.badge as badge
import simulation.scripts.tendency as tendency
import simulation.frivolity as frivolity
from logs.models import UpgradeLog

# fmt: off

# Class that holds methods that take us through the upgrade process
class UpgradeCreator:
    def __init__(self, user, player, data):
        self.player = player
        self.user = user
        self.data = data
        self.cart = {
            "total_sp": 0,
            "total_xp": 0,
            "attributes": {},
            "badges": {},
            "tendencies": {},
        }

    
    def compile_data(self):
        if type(self.player) == dict:
            self.player_attributes = self.player["attributes"]
            self.player_badges = self.player["badges"]
            self.player_tendencies = self.player["tendencies"]
        else:
            self.player_attributes = self.player.attributes
            self.player_badges = self.player.badges
            self.player_tendencies = self.player.tendencies

    # Remove attributes and badges that are the same as the players
    def format(self):
        # HTMX requests send a dictionary, Django sends a QueryDict
        self.compile_data()
        # Loop through the data and add the upgrades to the cart object if they have been changed
        for a, value in self.data.items():
            if not a in self.player_attributes: continue
            if int(value) > self.player_attributes[a]:
                self.cart["attributes"][a] = {}
                self.cart["attributes"][a]["start"] = self.player_attributes[a]
                self.cart["attributes"][a]["new"] = int(value)
        for b, value in self.data.items():
            if not b in self.player_badges: continue
            if int(value) > self.player_badges[b]:
                self.cart["badges"][b] = {}
                self.cart["badges"][b]["start"] = self.player_badges[b]
                self.cart["badges"][b]["new"] = int(value)
        for t, value in self.data.items():
            if not t in self.player_tendencies: continue
            if int(value) != self.player_tendencies[t]:
                self.cart["tendencies"][t] = {}
                self.cart["tendencies"][t]["start"] = self.player_tendencies[t]
                self.cart["tendencies"][t]["new"] = int(value)
        # Return an error message if the user has not selected any upgrades
        if not self.cart["attributes"] and not self.cart["badges"] and not self.cart["tendencies"]:
            return [False, "You have not selected any upgrades."]
        # Return a success message
        return [True, self.cart]

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
            self.cart["total_sp"] += price
        for b in self.cart["badges"]:
            start_value = self.cart["badges"][b]["start"]
            new_value = self.cart["badges"][b]["new"]
            price = badge.check_badge_price(start_value, new_value)
            self.cart["badges"][b]["price"] = price
            self.cart["total_sp"] += price
        for t in self.cart["tendencies"]:
            start_value = self.cart["tendencies"][t]["start"]
            new_value = self.cart["tendencies"][t]["new"]
            price = tendency.check_tendency_price(start_value, new_value)
            self.cart["tendencies"][t]["price"] = price
            self.cart["total_xp"] += price
        # Add surcharge (based on 'sp_spent') to the 'total_sp' price
        upgrade_surcharge = frivolity.get_surcharge_tier(self.player)
        if upgrade_surcharge:
            rounded_surcharge = round(self.cart["total_sp"] * upgrade_surcharge)
            self.cart["total_sp"] += rounded_surcharge
        # Check if user can afford the upgrades
        if validate:
            if self.user.sp < self.cart["total_sp"]:
                return [False, "You do not have enough SP to afford these upgrades."]
            if self.user.xp < self.cart["total_xp"]:
                return [False, "You do not have enough XP to afford these upgrades."]
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
        # Validate tendency upgrades
        for t, data in self.cart["tendencies"].items():
            if data["new"] > 100:
                return [False, f"You cannot upgrade {t} above 100."]
        # Return a success message
        return [True, self.cart]

    def push_upgrades(self, existing_log, data, upgrade_type):
        for item, data in data.items():
            item_upgraded = existing_log.upgrades[upgrade_type].get(item)
            if item_upgraded:
                item_upgraded["new"] = data["new"]
                item_upgraded["price"] += data["price"]
            else:
                existing_log.upgrades[upgrade_type][item] = data   
        existing_log.save()

    def purchase(self):

        return [False, "Player upgrades are currently disabled."]

        # Format the data
        validate_format = self.format()
        # Validate the user, price, and upgrades
        validate_user = self.validate_user()
        validate_price = self.validate_price()
        validate_upgrades = self.validate_upgrades()
        if validate_format[0] and validate_price[0] and validate_upgrades[0] and validate_user[0]:
            # Apply the upgrades & spent to the player
            for a, data in self.cart["attributes"].items():
                self.player.attributes[a] = data["new"]
            for b, data in self.cart["badges"].items():
                self.player.badges[b] = data["new"]
            for t, data in self.cart["tendencies"].items():
                self.player.tendencies[t] = data["new"]
            # Apply the price to the user
            self.user.sp -= self.cart["total_sp"]
            self.user.xp -= self.cart["total_xp"]
            self.player.sp_spent += self.cart["total_sp"]
            self.player.xp_spent += self.cart["total_xp"]
            self.user.save()
            self.player.save()
            # Log the upgrades
            # Check for existing upgrade log
            existing_log = UpgradeLog.objects.filter(player=self.player, complete=False).first()
            if existing_log:
                # Add the cost of SP & XP to the existing log
                existing_log.total_sp += self.cart["total_sp"]
                existing_log.total_xp += self.cart["total_xp"]
                # Add the upgrades to the existing log
                self.push_upgrades(existing_log, self.cart["attributes"], "attributes")
                self.push_upgrades(existing_log, self.cart["badges"], "badges")
                self.push_upgrades(existing_log, self.cart["tendencies"], "tendencies")
            else:
                UpgradeLog.objects.create(player=self.player, total_sp=self.cart["total_sp"], total_xp=self.cart["total_xp"], upgrades=self.cart)
            # Return a success message
            return [True, "Upgrades applied successfully."]
        else:
            errors = []
            if not validate_format[0]: errors.append(validate_format[1])
            if not validate_user[0]: errors.append(validate_user[1])
            if not validate_price[0]: errors.append(validate_price[1])
            if not validate_upgrades[0]: errors.append(validate_upgrades[1])
            return [False, errors]

# fmt: on
