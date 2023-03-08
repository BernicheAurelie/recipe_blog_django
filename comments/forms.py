from django.forms import ModelForm
from comments.models import Comment
from django import forms


class CreateComments(ModelForm):
    class Meta:
        CHOICES = [(0, '- 0'),(1, '- 1'), (2, '- 2'), (3, '- 3'), (4, '- 4'), (5, '- 5')]
        model = Comment
        fields = ['rating', 'title', 'description']
        widgets = {
            "rating": forms.RadioSelect(choices=CHOICES)
        }
