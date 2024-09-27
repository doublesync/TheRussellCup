# Python imports

# Third party imports

# Local imports
from players.models import Player
from accounts.models import CustomUser

# Create your tests here.
def run():

    for player in Player.objects.all():
        if player.user is not None:
            player.sp = player.user.sp
            player.xp = player.user.xp
            player.save()
    