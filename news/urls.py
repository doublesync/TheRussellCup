from django.urls import path

from news import views

urlpatterns = [
    path("", views.posts, name="posts"),
    path("post/<int:id>/", views.post, name="post"),
    path("post/create/", views.PostFormView.as_view(), name="create_post"),
    path("post/<int:id>/like/", views.htmx_create_like, name="create_like"),
]
