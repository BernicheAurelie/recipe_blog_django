from django.forms import ModelForm
from .models import Recipe


class CreateRecipe(ModelForm):
    class Meta:
        model = Recipe
        fields = ['title','ingredients', 'description', 'image', 'recipe_tag']
