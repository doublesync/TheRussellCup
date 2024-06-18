# Django imports
from django.urls import path

# Local imports
from news import views

# Create your urls here.
urlpatterns = [
    path("", views.posts, name="posts"),
    path("post/<int:pk>/", views.post, name="post"),
]
