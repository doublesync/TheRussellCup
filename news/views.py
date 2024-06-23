# Django imports
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic.edit import FormView

# Local imports
from news.models import Post, Like
from news.forms import PostForm
import simulation.webhook as webhook


# A view to get a post
def post(request, id):
    post = get_object_or_404(Post, id=id)
    return render(
        request,
        "news/post.html",
        {
            "post": post,
            "likes": Like.objects.filter(post=id).count(),
        },
    )


# A view to get all posts
def posts(request):
    # Get all posts (pagination is not implemented yet)
    posts = Post.objects.all()
    # Render posts
    return render(request, "news/posts.html", {"posts": posts})


# A view to create a post
class PostFormView(FormView):
    template_name = "news/create_post.html"
    form_class = PostForm

    def form_valid(self, form):
        if form.is_valid():
            # Create the post
            data = form.cleaned_data
            new_post = Post(
                user=self.request.user,
                title=data["title"],
                content=data["content"],
            )
            new_post.save()
            return redirect(post, new_post.id)


# A view to create a like
def htmx_create_like(request, id):
    # Create the like if one doesn't exist
    like_exists = Like.objects.filter(user=request.user, post=id).exists()
    if like_exists:
        Like.objects.filter(user=request.user, post=id).delete()
    else:
        new_like = Like(user=request.user, post=Post.objects.get(id=id))
        new_like.save()
    # Return the fragment to update the like count
    html = f'{Like.objects.filter(post=id).count()}'
    return HttpResponse(html)