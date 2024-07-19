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
    path("sort/<str:stat>/", views.sort_by_stat, name="sort_by_stat"),
    # path('season/<int:season_id>/', login_required(views.stats_season), name='stats_season'),
]