# Python imports

# Django imports
from django import forms

# Local imports
from news.models import Post


# Form for creating a post
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]
        labels = {
            "title": "Title",
            "content": "Content",
        }
        help_texts = {
            "title": "What's the title of your post?",
            "content": "What's the content of your post?",
        }
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control"}),
        }
