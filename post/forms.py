from django import forms
from .models import Post, Comment

class PostCreatedForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'title',
            'body',
            'image',
        )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("comment",)