# Python imports

# Django imports

# Local imports
import simulation.webhook as webhook
from simulation.scripts import animation as animation
from simulation.scripts import weight as weight

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
    webhook.send_webhook("specialty_rolls", title=f"🔥 {player.first_name} {player.last_name} has a new jumpshot!", body=jumpshot_string)
    # Return the player object and a message
    return [player, "✅ Jumpshot Roll applied, check the player page for the new animation."]

def modify_weight(player):
    # Apply the weight roll
    weight_roll_result = weight.weight_roll(player.position)
    # Set the weight roll results
    player.weight = weight_roll_result["weight"]
    player.attributes["Strength"] = weight_roll_result["strength"]
    # Create a string for the weight roll & send a webhook
    weight_string = f"Weight: {player.weight} lbs\nStrength: {player.attributes['Strength']}"
    webhook.send_webhook("specialty_rolls", title=f"🏋️ {player.first_name} {player.last_name} has a new weight!", body=weight_string)
    # Return the player object and a message
    return [player, f"✅ Weight Roll applied - Weight: {player.weight} lbs, Strength: {player.attributes['Strength']}"]

def modify_speed(player):
    # Define jumpshot speed
    timings_list = ["Very Slow", "Slow", "Normal", "Quick", "Very Quick"]
    timing = player.jumpshot_timing
    current = timings_list.index(timing) if timing in timings_list else None
    # Validate the current jumpshot timing
    if not current:
        return [player, "❌ The player does not have a jumpshot timing, cannot apply the speed increase."]
    if current >= 4:
        return [player, "❌ The player already has the fastest jumpshot timing, cannot apply the speed increase."]
    # Apply the speed increase
    player.jumpshot_timing = timings_list[current + 1]
    # Send a webhook
    webhook.send_webhook("specialty_rolls", title=f"🚀 {player.first_name} {player.last_name} has a faster jumpshot!", body=f"Jumpshot Timing: {player.jumpshot_timing}")
    # Return the player object and a message
    return [player, "✅ Speed Increase applied, the player now has a faster jumpshot timing."]
    
# Modification functions 
# Parameters: player object
# Returns: [player object, message]
MODIFICATION_FUNCTIONS = {
    '🔒 Jumpshot Roll': modify_jumpshot,
    '🔒 Weight Roll': modify_weight,
    'Shot Speed Increase (Guaranteed)': modify_speed,
}

# Checker function
def check_for_function(modification):
    if modification in MODIFICATION_FUNCTIONS:
        return MODIFICATION_FUNCTIONS[modification]
    return None
