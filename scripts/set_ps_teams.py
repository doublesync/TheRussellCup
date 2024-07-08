# Python imports

# Third party imports

# Local imports
from stats.models import PlayerGameStats

# Create your tests here.
def run():
    for player_game_stat in PlayerGameStats.objects.all():
        player_game_stat.set_team()
