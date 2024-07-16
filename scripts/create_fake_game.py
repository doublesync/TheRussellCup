# Python imports
import random

# Third party imports
from faker import Faker

# Local imports
from players.models import Player
from stats.models import Game, TeamGameStats, PlayerGameStats

# Create your tests here.
def run():
    game = Game.objects.create(
        surge_game=False,
        game_type="Regular Season",
        season_id=1,
        week=random.randint(1, 18),
        home_team_id=1,
        home_team_score=0,
        away_team_id=2,
        away_team_score=0,
        winner_id=None
    )
    players = Player.objects.all()
    for player in players:
        PlayerGameStats.objects.create(
            player_id=player.id,
            game_id=game.id,
            minutes_played=random.randint(0, 48),
            field_goals_made=random.randint(0, 20),
            field_goals_attempted=random.randint(0, 20),
            three_pointers_made=random.randint(0, 10),
            three_pointers_attempted=random.randint(0, 10),
            free_throws_made=random.randint(0, 10),
            free_throws_attempted=random.randint(0, 10),
            offensive_rebounds=random.randint(0, 10),
            defensive_rebounds=random.randint(0, 10),
            assists=random.randint(0, 10),
            steals=random.randint(0, 10),
            blocks=random.randint(0, 10),
            turnovers=random.randint(0, 10),
            personal_fouls=random.randint(0, 10),
            points=random.randint(0, 50),        
        )
