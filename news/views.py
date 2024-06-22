# Django imports
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic.edit import FormView

# Local imports
from news.models import Post, Like
from news.forms import PostForm
import simulation.webhook as webhook


# A view to get a post
def post(request, pk):
    # Check if post exists
    post_exists = Post.objects.filter(pk=pk).exists()
    # If post exists, render the post
    if post_exists:
        likes = Like.objects.filter(post=pk).count()
        return render(
            request, "news/post.html", {"post": Post.objects.get(pk=pk), "likes": likes}
        )
    else:
        return render(request, "500.html", {"reason": "Post does not exist"})


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
