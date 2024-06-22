# Django imports
from django.urls import path

# Local imports
from players import views

# Create your urls here.
urlpatterns = [
    path("create-player/", views.PlayerFormView.as_view(), name="create_player"),
    path("player/<int:id>/", views.player_page, name="player_page"),
]
