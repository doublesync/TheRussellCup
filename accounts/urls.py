from django.urls import path

from accounts import views

urlpatterns = [
    path("user/<int:id>/", views.user, name="user"),
    path("user/claim/", views.claim_contracts, name="claim_contracts"),
]
