# Django imports
from django.urls import path

# Local imports
from news import views

# Create your urls here.
urlpatterns = [
    path("", views.posts, name="posts"),
    path("post/<int:id>/", views.post, name="post"),
    path("post/create/", views.PostFormView.as_view(), name="create_post"),
]
