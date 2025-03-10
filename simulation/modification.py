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

# Activity rolls (temporary; change each season)
def activity_hotzone_roll(player):
     # Find out how many weeks the player has collected
     weeks_collected = 0
     if player.contract: 
         weeks_collected = len(player.contract.weeks_paid)
     if weeks_collected >= 6:
         # Give reward based on weeks collected
         roll = random.randint(1, 10)
         if roll == 1:
             return modify_hotzone(player)
         else:
             # Send webhook to the "rolls" channel
             webhook.send_webhook(
                 "specialty_rolls", 
                 title=f"😟 {player.first_name} {player.last_name} missed the hotzone!", 
                 body=f"You needed to roll a (1) to win, you rolled a {roll}..."
             )
             # Return the player object and a message
             return [player, f"😟 You needed to roll a (1) to win, you rolled a {roll}..."]
     else:
         return [player, "😟 You needed to collect for atleast 6 weeks to roll for a hotzone!"]
     
def activity_hidden_gem_roll(player):
     # Find out how many weeks the player has collected
     weeks_collected = 0
     if player.contract: 
         weeks_collected = len(player.contract.weeks_paid)
     # Give reward based on weeks collected
     if weeks_collected >= 12:
         # Roll for the hidden gem
         roll = random.randint(1, 50)
         if roll == 1:
             # Send webhook to the "rolls" channel
             webhook.send_webhook(
                 "specialty_rolls", 
                 title=f"🔥 {player.first_name} {player.last_name} is a Hidden Gem!", 
                 body="💎 (+5) to all physical attributes\n💎 (+5) to wingspan\n✔ Changes applied to website automatically"
             )
             # Apply the hidden gem
             player.attributes["Speed"] += 5
             player.attributes["Speed with Ball"] += 5
             player.attributes["Strength"] += 5
             player.attributes["Vertical"] += 5
             player.attributes["Agility"] += 5
             player.wingspan += 5
             # Return the player object and a message
             return [player, "🔥 Congratulations, this player is a Hidden Gem!"]
         else:
             # Send webhook to the "rolls" channel
             webhook.send_webhook(
                 "specialty_rolls", 
                 title=f"😟 {player.first_name} {player.last_name} missed the hidden gem!", 
                 body=f"You needed to roll a (1) to win, you rolled a {roll}..."
             )
             # Return the player object and a message
             return [player, f"😟 You needed to roll a (1) to win, you rolled a {roll}..."]
     else:
         return [player, "😟 You needed to collect for atleast 12 weeks to roll for a hidden gem!"]

# Modification functions 
# Parameters: player object
# Returns: [player object, message]
MODIFICATION_FUNCTIONS = {
    '🔒 Jumpshot Roll': modify_jumpshot,
    '🔒 Weight Roll': modify_weight,
    '🔒 Random Hot Zone': modify_hotzone,
    'Jumphot Speed Increase (Guaranteed)': modify_speed,
    '(S6) Activity Roll: Hotzone': activity_hotzone_roll,
    '(S6) Activity Roll: Hidden Gem': activity_hidden_gem_roll,
}

# Checker function
def check_for_function(modification):
    if modification in MODIFICATION_FUNCTIONS:
        return MODIFICATION_FUNCTIONS[modification]
    return None
