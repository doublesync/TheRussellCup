# Django imports
from django.urls import path

# Local imports
from players import views
from logs import views

# Create your urls here.
urlpatterns = [
    path("log/upgrade/<int:id>/", views.upgrade_log, name="upgrade_log"),
    path("log/payment/<int:id>/", views.payment_log, name="payment_log"),
    path("log/<int:id>/", views.view_logs, name="view_logs"),
    path("upgrades/incomplete/", views.IncompleteLogs.as_view(), name="incomplete_logs"),
    path("upgrade/<int:id>/complete/", views.mark_upgrade_complete, name="mark_upgrade_complete"),
    path("upgrades/incomplete/download/", views.download_incomplete_logs, name="download_incomplete_logs"),
]
