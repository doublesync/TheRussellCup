# Python imports

# Local imports
import simulation.config as config
import simulation.scripts.height as height
import simulation.scripts.weight as weight
import simulation.scripts.wingspan as wingspan
import simulation.scripts.animation as animation
import simulation.scripts.anomaly as anomaly
import simulation.scripts.physical as physical

from players.models import Player


# Class that holds methods that take us through the player creation process
class CreatePlayer:
    def __init__(self, first_name, last_name, position, number, country, college, user):
        # Instantiate the player object
        self.object = Player(
            first_name=first_name.title(),
            last_name=last_name.title(),
            position=position,
            number=number,
            country=country,
            college=college,
            user=user,
        )

    def validate(self):
        # Validate the max amount of players a user can have
        def validate_max_players():
            user = self.object.user
            count = Player.objects.filter(user=user).count()
            max_players = config.CONFIG_USER["MAX_PLAYERS"]
            if count >= max_players:
                return "You have reached the maximum amount of players."

        # Validate the background information
        def validate_background():
            country_length = len(self.object.country)
            college_length = len(self.object.college)
            if (country_length > 32) or (college_length > 32):
                return "Country and college names must be less than 32 characters."

        # List of validators
        validators = [validate_max_players, validate_background]
        # Run validators
        for validator in validators:
            validation = validator()
            if validation:
                return validation

    def generate(self):
        # Generate random fields
        self.object.height = height.height_roll(self.object.position)
        # [X] self.object.weight = weight.weight_roll(self.height) <= This is set in 'set_starting_physicals'
        self.object.wingspan = wingspan.wingspan_roll()
        self.object.jumpshot = animation.jumpshot_roll(self.object.height)
        # Set starting physicals and anomalies
        self.object = physical.set_starting_physicals(self.object)
        self.object = anomaly.anomaly_roll(self.object)
        # Return the player
        return self.object

    def create(self):
        # Validate the user
        validation = self.validate()
        if validation:
            return validation
        # Generate the player's random fields
        player = self.generate()
        # Set starting skill points and experience points
        self.object.user.sp += config.CONFIG_PLAYER["SP_DEFAULT"]
        self.object.user.xp += config.CONFIG_PLAYER["XP_DEFAULT"]
        # Save the player and user
        player.save()
        player.user.save()
        # Return the player
        return player
