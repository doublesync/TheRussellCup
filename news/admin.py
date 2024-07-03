# Django imports
from django.contrib import admin
from unfold.admin import ModelAdmin

# Local imports
from news.models import Post, Like

# Register your models here.

class PostAdmin(ModelAdmin):
    search_fields = ['title']
    autocomplete_fields = ['user']

admin.site.register(Post, PostAdmin)
admin.site.register(Like, ModelAdmin)
