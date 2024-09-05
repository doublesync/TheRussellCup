# Python imports

# Third party imports

# Local imports
import simulation.statfinder as statfinder

# Create your tests here.
def run():

    # Refresh the game high statistics
    finder = statfinder.StatFinder()
    finder.set_game_highs()