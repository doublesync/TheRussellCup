# User configuration
CONFIG_USER = {
    "MAX_PLAYERS": 1,
    "CARE_PACKAGE_MOD_DISCOUNT": 0.25,
}

# Season configuration
# Really this is just for limiting how much a player can earn each 'game week'
# It has no correlation to the seasons that will appear in the stats app
CONFIG_SEASON = {
    "CURRENT_WEEK": 0,
    "GAME_WEEK": 0,
    "CURRENT_SEASON": 3,
    "MAX_SP_WEEK": 90,
    "MAX_SP_SEASON": 1800,
    "CHECKIN_SP": 30,
    "CHECKIN_XP": 100,
    "DEFAULT_CONTRACT": 150,
}

# Player configuration
CONFIG_PLAYER = {
    "SP_DEFAULT": 5750,
    "SP_ANOMALY_BONUS": 1500, # 30% of the starting SP
    "XP_DEFAULT": 8500,
    "BADGE_LABELS": {
        0: "❌ None",
        1: "🟫 Bronze",
        2: "🌫️ Silver",
        3: "🟨 Gold",
        4: "🟪 Hall of Fame",
    },
    "SURCHARGE_TIERS": {
        1000: 0.02,
        2500: 0.05,
        5000: 0.10,
        7500: 0.15,
        10000: 0.20,
        15000: 0.30,
        20000: 0.40,
        25000: 0.50,
        30000: 0.60,
        40000: 0.80,
        50000: 1.00,
        60000: 1.20,
    }
}

CONFIG_STATS = {
    "TRACKED_TOTALS_FIELDS": [
        "minutes", "points", "rebounds", "assists", "steals", "blocks", "turnovers",
        "field_goals_made", "field_goals_attempted", "three_pointers_made", "three_pointers_attempted",
        "free_throws_made", "free_throws_attempted", "offensive_rebounds", "personal_fouls", 
        "plus_minus", "points_responsible_for", "dunks", "defensive_rebounds", "game_score", "effective_field_goal_percentage",
        "true_shooting_percentage", "turnover_percentage"
    ],
    "TRACKED_GAME_HIGH_FIELDS": [
        "points", "rebounds", "assists", "steals", "blocks", "turnovers",
        "field_goals_made", "field_goals_attempted", "three_pointers_made", "three_pointers_attempted",
        "free_throws_made", "free_throws_attempted", "offensive_rebounds", "personal_fouls", 
        "plus_minus", "points_responsible_for", "dunks", "defensive_rebounds", "game_score", "effective_field_goal_percentage",
        "true_shooting_percentage", "turnover_percentage"
    ],
}
