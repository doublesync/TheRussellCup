from django import forms

from news.models import Post


class PostForm(forms.ModelForm):
    """
    Form for creating and updating posts.
    """

    class Meta:
        """
        Meta class for PostForm.
        """

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
