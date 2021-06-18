from django import forms
from .models import Comments, Ice_Cream


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

class IceForm(forms.ModelForm):

    class Meta:
        model = Ice_Cream
        fields = ['name', 'images', 'price', 'size', 'categories', 'frequencies', 'description']