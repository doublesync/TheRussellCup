from players.models import Player
from logs.models import ContractLog

def run():
    players = Player.objects.all()
    for player in players:
        if not player.contract:
            contract = ContractLog.objects.create(
                player = player,
                season = 1,
                length = 1,
                option = "None",
                current_year_payment = 240,        
                incentives="None",        
            )
            player.contract = contract
            player.save()