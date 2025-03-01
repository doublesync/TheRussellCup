# User configuration
CONFIG_USER = {
    "MAX_PLAYERS": 1,
    "CARE_PACKAGE_MOD_DISCOUNT": 0.25,
}

# Season configuration
# Really this is just for limiting how much a player can earn each 'game week'
# It has no correlation to the seasons that will appear in the stats app
CONFIG_SEASON = {
    "CURRENT_WEEK": 9, # This controls the player/loser of the week updates
    "GAME_WEEK": 8, # This controls the payment week
    "CURRENT_SEASON": 6,
    "MAX_SP_WEEK": 90, # Deprecated (scared to remove it!)
    "MAX_SP_SEASON": 3000, # Raised from 2340 SP
    "CHECKIN_SP": 30,
    "CHECKIN_XP": 100,
    "DEFAULT_CONTRACT": 150,
    "FREE_AGENCY_OPEN": False, # This is the phase where players can be signed to contracts
}

# Player configuration
CONFIG_PLAYER = {
    "SP_DEFAULT": 7500, # Raised from 6000 SP
    "SP_ANOMALY_BONUS": 1500, # 30% of the starting SP
    "XP_DEFAULT": 9500, # Raised from 8500 XP
    "BADGE_LABELS": {
        0: "❌ None",
        1: "🟫 Bronze",
        2: "🌫️ Silver",
        3: "🟨 Gold",
        4: "🟪 Hall of Fame",
        5: "💎 Legend",
    },
    "SURCHARGE_STEP": 1000, # Every 1000 SP spent, the surcharge increases
    "SURCHARGE_INTEREST_INCREMENT": 0.02, # The surcharge interest rate increases by 2% for every 1000 SP spent
    "SURCHARGE_DEFAULT_INTEREST": 0.02, # The default surcharge interest rate
    "SURCHARGE_THRESHOLD": 1000, # The threshold for when the surcharge interest starts to apply
    "ROOKIE_CAP_HIT": 150, # The cap hit for a rookie player
    "ROLES": (
        ("Regular", "Regular"),
        ("Stash", "Stash"),
        ("First Option", "First Option"),
        ("Second Option", "Second Option"),
        ("Third Option", "Third Option"),
        ("Primary Scorer", "Primary Scorer"),
        ("Primary Playmaker", "Primary Playmaker"),
        ("On-Ball Defender", "On-Ball Defender")
    ),
}

CONFIG_STATS = {
    "TRACKED_TOTALS_FIELDS": [
        "minutes", "points", "rebounds", "assists", "steals", "blocks", "turnovers",
        "field_goals_made", "field_goals_attempted", "three_pointers_made", "three_pointers_attempted",
        "free_throws_made", "free_throws_attempted", "offensive_rebounds", "personal_fouls", 
        "plus_minus", "points_responsible_for", "dunks", "defensive_rebounds", "game_score", "effective_field_goal_percentage",
        "true_shooting_percentage", "turnover_percentage"
    ],
    "TRACKED_GAME_FIELDS": [
        "minutes", "rebounds", "assists", "steals", "blocks", "turnovers",
        "field_goals_made", "field_goals_attempted", "three_pointers_made", "three_pointers_attempted",
        "free_throws_made", "free_throws_attempted", "offensive_rebounds", "personal_fouls", 
        "plus_minus", "points_responsible_for", "dunks"
    ],   
    "TRACKED_GAME_HIGH_FIELDS": [
        "points", "rebounds", "assists", "steals", "blocks", "turnovers",
        "field_goals_made", "field_goals_attempted", "three_pointers_made", "three_pointers_attempted",
        "free_throws_made", "free_throws_attempted", "offensive_rebounds", "personal_fouls", 
        "plus_minus", "points_responsible_for", "dunks", "defensive_rebounds", "game_score", "effective_field_goal_percentage",
        "true_shooting_percentage", "turnover_percentage"
    ],
}
