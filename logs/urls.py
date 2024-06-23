# Django imports
from django.urls import path

# Local imports
from players import views
from logs import views

# Create your urls here.
urlpatterns = [
    path("log/upgrade/<int:id>/", views.upgrade_log, name="upgrade_log"),
    path("log/payment/<int:id>/", views.payment_log, name="payment_log"),
    path("logs/<int:id>/", views.view_logs, name="view_logs"),
]
