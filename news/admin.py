# Django imports
from django.contrib import admin

# Local imports
from news.models import Post, Like

# Register your models here.
admin.site.register(Post)
admin.site.register(Like)
