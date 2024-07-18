# User configuration
CONFIG_USER = {
    "MAX_PLAYERS": 1,
}

# Season configuration
# Really this is just for limiting how much a player can earn each 'game week'
# It has no correlation to the seasons that will appear in the stats app
CONFIG_SEASON = {
    "CURRENT_WEEK": 12,
    "CURRENT_SEASON": 1,
    "MAX_SP_WEEK": 90,
    "MAX_SP_SEASON": 1620,
    "CHECKIN_SP": 25,
    "CHECKIN_XP": 75,
}

# Player configuration
CONFIG_PLAYER = {
    "SP_DEFAULT": 5000,
    "SP_ANOMALY_BONUS": 1500, # 30% of the starting SP
    "XP_DEFAULT": 8500,
    "BADGE_LABELS": {
        0: "❌ None",
        1: "🟫 Bronze",
        2: "🌫️ Silver",
        3: "🟨 Gold",
        4: "🟪 Hall of Fame",
    },
}
