# Django imports
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Local imports
from news.models import Post, Like


# Create your views here.
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


def posts(request):
    # Get all posts
    posts = Post.objects.all()
    paginator = Paginator(posts, 10)
    page = request.GET.get("page")
    # Paginate posts
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    # Render posts
    return render(request, "news/posts.html", {"posts": posts})
