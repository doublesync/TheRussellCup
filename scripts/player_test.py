# Local imports
from simulation.scripts import physical as physical
from simulation.scripts import height as height
from simulation.scripts import weight as weight
from simulation.scripts import wingspan as wingspan
from simulation.scripts import animation as animation
from simulation.scripts import anomaly as anomaly

from players.models import Player
from teams.models import Team


# Create your tests here.
def run():
    hgt = height.height_roll("PG")
    new_player = Player(
        first_name="Russell",
        last_name="Westbrook",
        position="PG",
        number=26,
        height=hgt,
        wingspan=wingspan.wingspan_roll(),
        jumpshot=animation.jumpshot_roll(hgt),
    )
    updated_player = physical.set_starting_physicals(new_player)
    updated_player = anomaly.anomaly_roll(updated_player)
    updated_player.save()
