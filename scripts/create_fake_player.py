# # Python imports
# import random

# # Django imports
# from django.utils import timezone

# # Third party imports
# import factory

# # Local imports
# from accounts.models import CustomUser as User
# from players.models import Player
# from teams.models import Team
# from stats.models import Season, Game, TeamGameStats, PlayerGameStats

# season = Season.objects.get(pk=1)
# user = User.objects.get(pk=1)

# class TeamFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = Team

#     manager = user
#     name = factory.Faker('company')
#     city = factory.Faker('city')

# class PlayerFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = Player

#     first_name = factory.Faker('first_name')
#     last_name = factory.Faker('last_name')
#     number = random.randint(0, 99)
#     position = random.choice(['PG', 'SG', 'SF', 'PF', 'C'])
#     height = random.randint(60, 90)
#     weight = random.randint(150, 300)
#     wingspan = random.randint(60, 90)
#     college = factory.Faker('company')
#     country = factory.Faker('country')
#     jumpshot = "Test Jumpshot"

# class GameFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = Game

#     game_type = random.choice(['Regular', 'Playoff', 'Final'])
#     home_team_score = random.randint(50, 150)
#     away_team_score = random.randint(50, 150)
#     week = random.randint(1, 18)
#     season = season

# class PlayerGameStatsFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = PlayerGameStats

#     game = factory.SubFactory(GameFactory)
#     team = factory.SubFactory(TeamFactory)
#     player = factory.SubFactory(PlayerFactory)
#     minutes = random.randint(0, 48)
#     points = random.randint(0, 50)
#     rebounds = random.randint(0, 20)
#     assists = random.randint(0, 15)
#     steals = random.randint(0, 10)
#     blocks = random.randint(0, 10)
#     turnovers = random.randint(0, 10)
#     field_goals_made = random.randint(0, 20)
#     field_goals_attempted = random.randint(0, 30)
#     three_pointers_made = random.randint(0, 10)
#     three_pointers_attempted = random.randint(0, 15)
#     free_throws_made = random.randint(0, 10)
#     free_throws_attempted = random.randint(0, 15)
#     offensive_rebounds = random.randint(0, 10)
#     personal_fouls = random.randint(0, 5)
#     plus_minus = random.randint(-10, 10)
#     points_responsible_for = random.randint(0, 50)
#     dunks = random.randint(0, 5)

# class TeamGameStatsFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = TeamGameStats

#     team = factory.SubFactory(TeamFactory)
#     game = factory.SubFactory(GameFactory)
#     field_goals_made = random.randint(0, 50)
#     field_goals_attempted = random.randint(0, 70)
#     three_pointers_made = random.randint(0, 20)
#     three_pointers_attempted = random.randint(0, 30)
#     free_throws_made = random.randint(0, 20)
#     free_throws_attempted = random.randint(0, 30)
#     fast_break_points = random.randint(0, 20)
#     points_in_paint = random.randint(0, 50)
#     second_chance_points = random.randint(0, 20)
#     bench_points = random.randint(0, 20)
#     assists = random.randint(0, 30)
#     offensive_rebounds = random.randint(0, 20)
#     defensive_rebounds = random.randint(0, 20)
#     steals = random.randint(0, 20)
#     blocks = random.randint(0, 20)
#     turnovers = random.randint(0, 20)
#     points_off_turnovers = random.randint(0, 50)
#     personal_fouls = random.randint(0, 20)
#     dunks = random.randint(0, 10)
#     biggest_lead = random.randint(0, 50)
#     time_of_possession = timezone.timedelta(minutes=random.randint(0, 48))

# # Create your tests here.
# def run():
#     for _ in range(100):
#         from django import db
#         db.connections.close_all()
#         # # We need to make 10 different PlayerGameStats for ecah game, and 2 different TeamGameStats
#         # home_team, away_team = TeamFactory.create(), TeamFactory.create()
#         # game = GameFactory.create(home_team=home_team, away_team=away_team)
#         # # If not more than 100 players, create them, if more than 100, get them
#         # players = PlayerFactory.create_batch(10)
#         # for player in players:
#         #     PlayerGameStatsFactory.create(player=player, game=game)
#         # TeamGameStatsFactory.create(team=home_team, game=game)
#         # TeamGameStatsFactory.create(team=away_team, game=game)
