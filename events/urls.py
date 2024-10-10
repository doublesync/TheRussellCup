# Django imports
from django.contrib.auth.decorators import login_required
from django.urls import path

# Local imports
from events import views

# Create your urls here.
urlpatterns = [
    # fmt:off
    path("list/", views.events_list, name="events_list"),
    path("view/<int:id>/", views.view_event, name="view_event"),
    path("add_entry/", views.add_entry, name="add_entry"),
    # fmt:on
]
