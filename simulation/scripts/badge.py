# Badge categories
badge_categories = {
    "Shooting": [
        "Agent 3",
        "Blinders",
        "Catch & Shoot",
        "Claymore",
        "Comeback Kid",
        "Corner Specialist",
        "Deadeye",
        "Free Points",
        "Green Machine",
        "Guard Up",
        "Limitless Range",
        "Middy Magician",
        "Open Looks",
        "Post Fade Phenom",
        "Slippery Off-Ball",
        "Space Creator",
        "Spot Finder",
    ],
    "Playmaking": [
        "Ankle Breaker",
        "Bail Out",
        "Blow-By",
        "Break Starter",
        "Dimer",
        "Handles for Days",
        "Hyperdrive",
        "Killer Combos",
        "Needle Threader",
        "Physical Handles",
        "Post Playmaker",
        "Relay Passer",
        "Special Delivery",
        "Speed Booster",
        "Touch Passer",
        "Triple Spike",
        "Unpluckable",
    ],
    "Finishing": [
        "Acrobat",
        "Aerial Wizard",
        "Backdown Punisher",
        "Big Driver",
        "Bulldozer",
        "Bunny",
        "Dream Shake",
        "Dropstepper",
        "Fast Twitch",
        "Fearless Finisher",
        "Float Game",
        "Giant Slayer",
        "Hook Specialist",
        "Masher",
        "Post Spin Technician",
        "Posterizer",
        "Precision Dunker",
        "Pro Touch",
        "Rise Up",
        "Scooper",
        "Slithery",
        "Spin Cycle",
        "Two Step",
        "Whistle",
    ],
    "Defensive": [
        "94 Feet",
        "Anchor",
        "Ankle Braces",
        "Boxout Beast",
        "Brick Wall",
        "Challenger",
        "Chase Down Artist",
        "Clamps",
        "Fast Feet",
        "Glove",
        "Interceptor",
        "Immovable Enforcer",
        "Off-Ball Pest",
        "Pick Dodger",
        "Pogo Stick",
        "Post Lockdown",
        "Rebound Chaser",
        "Right Stick Ripper",
        "Work Horse",
    ],
}

# Badge prices (in SP)
badge_prices = {
    1: 100,
    2: 150,
    3: 300,
    4: 600,
}


# Checks the price of a badge and returns the cost
def check_badge_price(start_level, end_level):
    cost = 0
    start, end = (start_level + 1), (end_level + 1)
    for i in range(start, end):
        cost += badge_prices[i]
    return cost


# Checks if a player is eligible for a badge at a certain level and returns the result
def eligible_for_badge(player, badge, badge_level):
    return True
