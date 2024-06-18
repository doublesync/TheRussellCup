# Django imports
from django.urls import path

# Local imports
from accounts import views

# Create your urls here.
urlpatterns = [path("profile/<int:pk>/", views.user, name="user")]
