# 2K25 Badge System
refundable_badges = [
    "Giant Slayer",
    "Masher",
    "Pro Touch",
    "Slithery",
    "Bunny",
    "Precision Dunker",
    "Whistle",
    "Comeback Kid",
    "Corner Specialist",
    "Green Machine",
    "Guard Up",
    "Space Creator",
    "Free Points",
    "Open Looks",
    "Hyperdrive",
    "Killer Combos",
    "Post Playmaker",
    "Big Driver",
    "Blow-By",
    "Relay Passer",
    "Touch Passer",
    "Triple Spike",
    "Ankle Braces",
    "Work Horse",
    "Fast Feet",
    "Right Stick Ripper",
    "Bulldozer",
]

# If multiple badges convert to the same new bdage
# Convert to the 'max'
convertable_badges = {
    "Acrobat": "Layup Mixmaster",
    "Scooper": "Layup Mixmaster",
    "Spin Cycle": "Layup Mixmaster",
    "Two Step": "Layup Mixmaster",
    "Backdown Punisher": "Post Powerhouse",
    "Dropstepper": "Post Powerhouse",
    "Dream Shake": "Post-Up Poet",
    "Post Spin Technician": "Post-Up Poet",
    "Blinders": "Deadeye",
    "Catch & Shoot": "Set Shot Specialist",
    "Claymore": "Set Shot Specialist",
    "Agent 3": "Shifty Shooter",
    "Middy Magician": "Shifty Shooter",
    "Ankle Breaker": "Ankle Assassin",
    "Speed Booster": "Lightning Launch",
    "Physical Handles": "Strong Handle",
    "Needle Threader": "Versatile Visionary",
    "Special Delivery": "Versatile Visionary",
    "Chase Down Artist": "High-Flying Denier",
    "Clamps": "On-Ball Menace",
    "Anchor": "Paint Patroller",
    "Fast Twitch": "Paint Prodigy",
    "Fearless Finisher": "Physical Finisher",
}

# Badge categories
badge_categories = {
    "Inside Scoring": [
        "Aerial Wizard",
        "Float Game",
        "Hook Specialist",
        "Layup Mixmaster",
        "Paint Prodigy",
        "Physical Finisher",
        "Post Fade Phenom",
        "Post Powerhouse",
        "Post-Up Poet",
        "Posterizer",
        "Rise Up",
    ],
    "Outside Scoring": [
        "Deadeye",
        "Limitless Range",
        "Mini Marksman",
        "Set Shot Specialist",
        "Shifty Shooter",
        "Slippery Off-Ball",
    ],
    "Playmaking": [
        "Ankle Assassin",
        "Bail Out",
        "Break Starter",
        "Dimer",
        "Handles for Days",
        "Lightning Launch",
        "Strong Handle",
        "Unpluckable",
        "Versatile Visionary",
    ],
    "Defense": [
        "Challenger",
        "Glove",
        "High-Flying Denier",
        "Interceptor",
        "Off-Ball Pest",
        "On-Ball Menace",
        "Paint Patroller",
        "Pick Dodger",
        "Post Lockdown",
        "Pogo Stick",
    ],
    "Athleticism": [
        "Brick Wall",
        "Immovable Enforcer",
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
