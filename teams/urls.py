# Django imports
from django.urls import path

# Local imports
from teams import views

# Create your urls here.
urlpatterns = [
    path("list/", views.team_list, name="team_list"),
    path("team/<int:id>/", views.team_page, name="team_page"),
    path("drafts/list/", views.draft_list, name="draft_list"),
    path("draft/<int:id>/", views.draft_page, name="draft_page"),
]
