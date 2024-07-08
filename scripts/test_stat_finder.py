# Python imports
import json

# Third party imports

# Local imports
import simulation.statfinder as statfinder
from players.models import Player

# Create your tests here.
def run():
    player = Player.objects.get(pk=23)
    stat_finder = statfinder.StatFinder()
    print(json.dumps(stat_finder.player_totals(player=player), indent=4, sort_keys=True, default=str))
    print(json.dumps(stat_finder.team_totals(team=player.team), indent=4, sort_keys=True, default=str))