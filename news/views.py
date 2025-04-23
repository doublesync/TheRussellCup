from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.views.generic.edit import FormView

from news.forms import PostForm
from news.models import Like, Post


def post(request, id):
    """
    A view to get a post by id
    """
    post = get_object_or_404(Post, pk=id)
    return render(
        request,
        "news/post.html",
        {
            "post": post,
            "likes": Like.objects.filter(post=post).count(),
        },
    )


def posts(request):
    """
    A view to get all posts
    """

    return render(
        request, "news/posts.html", {"posts": Post.objects.all().order_by("-created")}
    )


class PostFormView(FormView):
    """
    A view to create a post
    """

    template_name = "news/create_post.html"
    form_class = PostForm

    def form_valid(self, form):
        """
        If the form is valid, save the post and redirect to the post detail view.
        """
        new_post = form.save(commit=False)  # Use Django's built-in form save method
        new_post.user = self.request.user  # Assign the current user to the post
        new_post.save()
        return redirect(
            "post", id=new_post.id
        )  # Use named URL patterns for better maintainability


@require_POST
def htmx_create_like(request, id):
    """
    A view to toggle a like for a post
    """

    post = get_object_or_404(Post, id=id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if not created:
        like.delete()

    like_count = Like.objects.filter(post=post).count()
    return HttpResponse(like_count, content_type="text/plain")
