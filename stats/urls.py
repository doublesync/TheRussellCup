# Django imports
from django.contrib.auth.decorators import login_required
from django.urls import path

# Local imports
from stats import views

# Create your urls here.
urlpatterns = [
    # path('', login_required(views.stats_home), name='stats_home'),
    # path('list/', login_required(views.stats_list), name='stats_list'),
    path('players/<int:id>/', login_required(views.stats_player), name='stats_player'),
    path('teams/<int:id>/', login_required(views.stats_teams), name='stats_teams'),
    # path('season/<int:season_id>/', login_required(views.stats_season), name='stats_season'),
]