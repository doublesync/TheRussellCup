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
    "MAX_SP_SEASON": 2340, # Raised from 1800 SP
    "CHECKIN_SP": 30,
    "CHECKIN_XP": 100,
    "DEFAULT_CONTRACT": 150,
}

# Player configuration
CONFIG_PLAYER = {
    "SP_DEFAULT": 6000, # Raised from 5750 SP
    "SP_ANOMALY_BONUS": 1500, # 30% of the starting SP
    "XP_DEFAULT": 8500,
    "BADGE_LABELS": {
        0: "❌ None",
        1: "🟫 Bronze",
        2: "🌫️ Silver",
        3: "🟨 Gold",
        4: "🟪 Hall of Fame",
    },
    "SURCHARGE_STEP": 1000, # Every 1000 SP spent, the surcharge increases
    "SURCHARGE_INTEREST_INCREMENT": 0.04, # The surcharge interest rate increases by 4% for every 1000 SP spent
    "SURCHARGE_DEFAULT_INTEREST": 0.04, # The default surcharge interest rate
    "SURCHARGE_THRESHOLD": 1000, # The threshold for when the surcharge interest starts to apply
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
