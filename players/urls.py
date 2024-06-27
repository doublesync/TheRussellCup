# Django imports
from django.contrib.auth.decorators import login_required
from django.urls import path

# Local imports
from players import views

# Create your urls here.
urlpatterns = [
    # fmt:off
    path("create-player/", views.PlayerFormView.as_view(), name="create_player"),
    path("player/<int:id>/", views.player_page, name="player_page"),
    path("player/<int:id>/upgrade/", views.UpgradeFormView.as_view(), name="upgrade_page"),
    path("list/", views.PlayerListView.as_view(), name="player_list"),
    path("player/<int:id>/appearance/", login_required(views.EditAppearanceView.as_view()), name="edit_appearance"),
    path("player/list/search/", views.htmx_search_players, name="htmx_search_players"),
    # fmt:on
]
