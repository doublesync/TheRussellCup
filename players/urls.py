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
    path("player/list/search/<str:model>/", views.htmx_filter_players, name="htmx_filter_players"),
    path("player/mods/list/", views.ModificationsListView.as_view(), name="mods_list"),
    path("player/mods/purchase/<int:id>/", views.purchase_modification, name="purchase_modification"),
    path("player/<int:id>/upgrade/advice/", views.htmx_upgrade_advice, name="htmx_upgrade_advice"),
    path("player/trophyrack/<int:id>/", views.TrophyRackView.as_view(), name="trophy_rack"),
    path("compare/", views.ComparePlayersView.as_view(), name="compare_players"),
    path("compare/change/", views.htmx_compare_players, name="htmx_compare_players"),
    path("player/<int:id>/animations/", views.PlayerAnimationsView.as_view(), name="player_animations"),
    path("player/<int:id>/styles/", views.PlayerStylesView.as_view(), name="player_styles"),
    path("player/<int:id>/styles/update/", views.htmx_update_player_styles, name="htmx_update_player_styles"),
    # fmt:on
]
