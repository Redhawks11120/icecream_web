from django import forms
from .models import Comments


class CommentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author', None)
        self.post = kwargs.pop('post', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        comments = super().save(commit=False)
        comments.author = self.author
        comments.post = self.post
        comments.save()

    class Meta:
        model = Comments
        fields = ["body"]
