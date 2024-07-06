# Badge categories
badge_categories = {
    "Inside Scoring": [
        "Acrobat",
        "Aerial Wizard",
        "Backdown Punisher",
        "Dream Shake",
        "Dropstepper",
        "Fast Twitch",
        "Fearless Finisher",
        "Giant Slayer",
        "Masher",
        "Post Spin Technician",
        "Posterizer",
        "Pro Touch",
        "Rise Up",
        "Slithery",
        "Bunny",
        "Float Game",
        "Hook Specialist",
        "Precision Dunker",
        "Scooper",
        "Spin Cycle",
        "Two Step",
        "Whistle",
    ],
    "Outside Scoring": [
        "Agent 3",
        "Blinders",
        "Catch & Shoot",
        "Claymore",
        "Comeback Kid",
        "Corner Specialist",
        "Deadeye",
        "Green Machine",
        "Guard Up",
        "Limitless Range",
        "Middy Magician",
        "Slippery Off-Ball",
        "Space Creator",
        "Free Points",
        "Open Looks",
        "Post Fade Phenom",
        "Spot Finder",
    ],
    "Playmaking": [
        "Ankle Breaker",
        "Bail Out",
        "Break Starter",
        "Dimer",
        "Handles for Days",
        "Hyperdrive",
        "Killer Combos",
        "Needle Threader",
        "Post Playmaker",
        "Special Delivery",
        "Unpluckable",
        "Big Driver",
        "Blow-By",
        "Physical Handles",
        "Relay Passer",
        "Speed Booster",
        "Touch Passer",
        "Triple Spike",
    ],
    "Defense": [
        "Anchor",
        "Ankle Braces",
        "Challenger",
        "Chase Down Artist",
        "Clamps",
        "Glove",
        "Interceptor",
        "Off-Ball Pest",
        "Pick Dodger",
        "Post Lockdown",
        "Pogo Stick",
        "Work Horse",
        "Fast Feet",
        "Right Stick Ripper",
    ],
    "Athleticism": [
        "Brick Wall",
        "Bulldozer",
        "Immovable Enforcer",
        "94 Feet",
    ],
    "Rebounding": [
        "Boxout Beast",
        "Rebound Chaser",
    ]
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

def order_badges(badges):
    # Order the badges by their categories
    ordered_badges = {}
    for category in badge_categories:
        ordered_badges[category] = {}
        for badge in badge_categories[category]:
            if badge in badges:
                ordered_badges[category][badge] = badges[badge]
    return ordered_badges
