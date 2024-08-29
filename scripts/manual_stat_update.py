# Python imports

# Third party imports

# Local imports
from stats.models import TeamSeasonStats, PlayerSeasonStats

# Create your tests here.
def run():

    # Initialize the team and player season stats
    team_season_stats = TeamSeasonStats.objects.all()
    player_season_stats = PlayerSeasonStats.objects.all()

    # Update the team and player season stats
    for season_stats in team_season_stats:
        season_stats.save()

    for season_stats in player_season_stats:
        season_stats.save()
