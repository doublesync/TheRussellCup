# Python imports

# Django imports

# Local imports
import simulation.webhook as webhook
from simulation.scripts import animation as animation


# Modification connector functions 
def modify_jumpshot(player):
    # Apply the jumpshot roll
    player = animation.generate_jumpshot(player)
    # Create a string for the jumpshot & send a webhook
    jumpshot_string = f"""Base: {player.jumpshot}
    Release 1: {player.jumpshot_release_1}
    Release 2: {player.jumpshot_release_2}
    Blending: {player.jumpshot_blending}
    Timing: {player.jumpshot_timing}
    Free Throw: {player.jumpshot_free_throw}"""
    webhook.send_webhook("jumpshot_rolls", title=f"🔥 {player.first_name} {player.last_name} has a new jumpshot!", body=jumpshot_string)
    # Return the player object and a message
    return [player, "✅ Jumpshot Roll applied, check on the players page for the new animation."]

# Modification functions 
# Parameters: player object
# Returns: [player object, message]
MODIFICATION_FUNCTIONS = {
    'Jumpshot Roll': modify_jumpshot,
}

# Checker function
def check_for_function(modification):
    if modification in MODIFICATION_FUNCTIONS:
        return MODIFICATION_FUNCTIONS[modification]
    return None