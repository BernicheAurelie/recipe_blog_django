from django.forms import ModelForm, Textarea
from .models import Recipe


class CreateRecipe(ModelForm):
    class Meta:
        model = Recipe
        fields = ['title','ingredients', 'description', 'image', 'recipe_tag']
        widgets = {
            "ingredients": Textarea(attrs={"cols": 80, "rows": 20}),
            "description": Textarea(attrs={"cols": 80, "rows": 20}),
        }
