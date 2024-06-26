# Django imports
from django.contrib.auth.decorators import login_required
from django.urls import path

# Local imports
from stafftools import views

# Create your urls here.
urlpatterns = [
    # fmt:off
    path("payuser/<int:id>/", views.pay_user, name="pay_user"),
    # fmt:on
]
