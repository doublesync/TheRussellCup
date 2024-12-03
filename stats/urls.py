# Django imports
from django.contrib.auth.decorators import login_required
from django.urls import path

# Local imports
from stats import views

# Create your urls here.
urlpatterns = [
    path("", views.stats_home, name="stats_home"),
    path("records/", views.records, name="records"),
    path("performances/", views.performances, name="performances"),
    path("averages/players/", views.player_averages, name="player_averages"),
    path("sort/<str:stat>/", views.sort_by_stat, name="sort_by_stat"),
    path("games/recent/player/<int:id>/", views.recent_season_games, name="recent_season_games"),
    path("games/create/", views.create_game, name="create_game"),
    path("boxscore/<int:id>/", views.boxscore, name="boxscore"),
    path("averages/league/", views.league_averages, name="league_averages"),
    path("api/league/", views.league_stats_api, name="league_stats_api"),
    path("games/create/roster/", views.htmx_fetch_roster, name="htmx_fetch_roster"),
]