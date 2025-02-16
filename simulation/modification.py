# Python imports
import random

# Django imports

# Local imports
import simulation.webhook as webhook
from simulation.scripts import animation as animation
from simulation.scripts import weight as weight

# Configurations
hotzone_list = {
    14: "Inside Center",
    13: "Inside Right",
    12: "Inside Free Throw",
    11: "Inside Left",
    10: "Mid-Range Right Corner",
    9: "Mid-Range Right Wing",
    8: "Mid-Range Middle",
    7: "Mid-Range Left Wing",
    6: "Mid-Range Left Corner",
    5: "Three Right Corner",
    4: "Three Right Wing",
    3: "Three Middle",
    2: "Three Left Wing",
    1: "Three Left Corner",
}

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

def modify_hotzone(player):
    # 10% chance to be cold, 90% chance to be hot
    hot_roll = random.randint(1, 10)
    hot = True if (hot_roll < 10) else False
    # Roll for the type of hotzone
    area_roll = random.randint(1, 14)
    hotzone = hotzone_list[area_roll]
    # Send the webhook for the hotzone
    webhook.send_webhook("specialty_rolls", title=f"{'🔥' if hot else '🧊'} {player.first_name} {player.last_name} has a new hotzone!", body=f"{hotzone} - {'Hot' if hot else 'Cold'}")
    # Return the player object and a message
    return [player, f"✅ Hotzone Roll applied: {hotzone} - {'Hot' if hot else 'Cold'}"]

def activity_physicals_roll(player):
    # Find out how many weeks the player has collected
    weeks_collected = 0
    if player.contract: 
        weeks_collected = len(player.contract.weeks_paid)
    # Give reward based on weeks collected
    if weeks_collected >= 0:
        # Roll for the physicals boost
        roll = random.randint(1, 50)
        if roll == 1:
            # Send webhook to the "rolls" channel
            webhook.send_webhook(
                "specialty_rolls", 
                title=f"🔥 {player.first_name} {player.last_name} has won a Physical boost.", 
                body="(+3) to all physical attributes (including wingspan)\n✔ Changes applied to website automatically"
            )
            # Apply the physicals boost
            player.attributes["Speed"] += 3
            player.attributes["Speed with Ball"] += 3
            player.attributes["Strength"] += 3
            player.attributes["Vertical"] += 3
            player.attributes["Agility"] += 3
            player.wingspan += 3
            # Return the player object and a message
            return [player, "🔥 Congratulations, this player won a Physical Boost!"]
        else:
            # Send webhook to the "rolls" channel
            webhook.send_webhook(
                "specialty_rolls", 
                title=f"😟 {player.first_name} {player.last_name} missed the Physical Boost!", 
                body=f"You needed to roll a (1) to win, you rolled a {roll}..."
            )
            # Return the player object and a message
            return [player, f"😟 You needed to roll a (1) to win, you rolled a {roll}..."]
    else:
        return [player, "😟 You needed to collect for atleast 15 weeks to roll for a physical boost!"]

def activity_anomaly_roll(player):
    # Roll for the anomaly
    roll = random.randint(1, 100)
    if roll == 1:
        if player.anomaly:
            player.sp += 800
            return [player, "🔥 Already an anomaly; wins 800SP!"]
        else:
            # Send webhook to the "rolls" channel
            webhook.send_webhook(
                "specialty_rolls", 
                title=f"🔥 {player.first_name} {player.last_name} is now an ANOMALY.", 
                body="✔ Changes applied to website automatically, go check them out!"
            )
            # Apply the anomaly
            player.height += random.randint(1, 3)
            player.wingspan += random.randint(3, 7)
            player.attributes["Speed"] += random.randint(1, 5)
            player.attributes["Speed with Ball"] += random.randint(1, 5)
            player.attributes["Strength"] += random.randint(1, 5)
            player.attributes["Vertical"] += random.randint(1, 5)
            player.attributes["Agility"] += random.randint(1, 5)
            # Return the player object and a message
            return [player, "🔥 Congratulations, this player won is now an ANOMALY!"]
    else:
        # Send webhook to the "rolls" channel
        webhook.send_webhook(
            "specialty_rolls", 
            title=f"😟 {player.first_name} {player.last_name} missed the anomaly roll!", 
            body=f"You needed to roll a (1) to win, you rolled a {roll}..."
        )
        # Return the player object and a message
        return [player, f"😟 You needed to roll a (1) to win, you rolled a {roll}..."]

# Modification functions 
# Parameters: player object
# Returns: [player object, message]
MODIFICATION_FUNCTIONS = {
    '🔒 Jumpshot Roll': modify_jumpshot,
    '🔒 Weight Roll': modify_weight,
    '🔒 Random Hot Zone': modify_hotzone,
    'Jumphot Speed Increase (Guaranteed)': modify_speed,
    'Activity Roll: Physicals': activity_physicals_roll,
    'Activity Roll: Anomaly': activity_anomaly_roll,
}

# Checker function
def check_for_function(modification):
    if modification in MODIFICATION_FUNCTIONS:
        return MODIFICATION_FUNCTIONS[modification]
    return None
