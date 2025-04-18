from django.urls import path

from events import views

urlpatterns = [
    path("list/", views.events_list, name="events_list"),
    path("view/<int:event_id>/", views.view_event, name="view_event"),
    path("add/entry/", views.AddEntryView.as_view(), name="add_entry"),
]
