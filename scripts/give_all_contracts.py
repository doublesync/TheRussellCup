# Python imports

# Third party imports

# Local imports
from players.models import Player
from logs.models import ContractLog

# Create your tests here.
def run():
    for player in Player.objects.all():
        contract = ContractLog.objects.create(
            player=player,
            season=1,
            length=1,
            option="Team Option",
            current_year_payment=240,
            incentives="None",
        )
        player.contract = contract
        player.save()
        print(contract)
