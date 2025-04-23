from django.contrib import admin
from unfold.admin import ModelAdmin

from news.models import Like, Post


class PostAdmin(ModelAdmin):
    """
    Admin interface for the Post model.
    """

    search_fields = ["title"]
    autocomplete_fields = ["user"]


admin.site.register(Post, PostAdmin)
admin.site.register(Like, ModelAdmin)
