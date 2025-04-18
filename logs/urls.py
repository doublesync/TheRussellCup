from django.urls import path

from logs import views

urlpatterns = [
    path("log/upgrade/<int:log_id>/", views.upgrade_log, name="upgrade_log"),
    path("log/payment/<int:log_id>/", views.payment_log, name="payment_log"),
    path("log/<int:log_id>/", views.view_logs, name="view_logs"),
    path("upgrades/", views.IncompleteLogs.as_view(), name="incomplete_logs"),
    path(
        "upgrade/<int:log_id>/complete/",
        views.mark_upgrade_complete,
        name="mark_upgrade_complete",
    ),
    path(
        "upgrades/download/",
        views.download_incomplete_logs,
        name="download_incomplete_logs",
    ),
    path(
        "upgrades/all/complete/",
        views.mark_all_upgrades_complete,
        name="mark_all_upgrades_complete",
    ),
]
