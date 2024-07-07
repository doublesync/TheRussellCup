# Django imports
from django.urls import path

# Local imports
from accounts import views

# Create your urls here.
urlpatterns = [
    path("profile/<int:id>/", views.user, name="user"),
    path("user/contracts/claim/", views.claim_contracts, name="claim_contracts")
]
