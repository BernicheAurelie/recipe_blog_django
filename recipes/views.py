from itertools import chain
import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import CharField, Value, Q
from django.contrib import messages
from comments.models import Comment
from .forms import CreateRecipe
from .models import Recipe


def recipes_index(request):
    titre = "Bienvenue sur notre forum culinaire"
    today = datetime.date.today()
    recipes = Recipe.objects.all()
    comments = Comment.objects.all()
    if request.method == "GET":
        name = request.GET.get("recherche")
        if name is not None:
            recipes = Recipe.objects.filter(Q(title__icontains=name)| Q(ingredients__icontains=name)| Q(description__icontains=name)|Q(recipe_tag__icontains=name))
            if not recipes:
                message = "Il n'y a pas encore de recette correspondant à la recherche."
                context = {"titre": titre,'message':message}
                return render(request, 'recipes/recipes.html', context)
    recipes = recipes.annotate(content_type=Value('RECIPE', CharField()))
    # comments = comments.annotate(content_type=Value('COMMENT', CharField()))
    posts = sorted(recipes,
            key=lambda post: post.time_created,
            reverse=True
        )
    context = {"titre": titre, 'posts': posts, 'comments': comments, 'today': today}
    return render(request, 'recipes/recipes.html', context)

@login_required(login_url='connexion')
def my_recipes(request):
    titre = "Bienvenue sur ta page de recettes"
    context = {"titre": titre}
    user = request.user
    recipes = Recipe.objects.filter(user__exact=user)
    if recipes:
        if request.method == "GET":
            name = request.GET.get("recherche")
            if name is not None:
                recipes = Recipe.objects.filter(Q(title__icontains=name)| Q(ingredients__icontains=name)| Q(description__icontains=name)|Q(recipe_tag__icontains=name))
                if not recipes:
                    message = "Il n'y a pas encore de recette correspondant à ta recherche. "
                    context = {"titre": titre,'message':message}
                    return render(request, 'recipes/recipes.html', context)
        recipes = sorted(recipes, key=lambda recipe: recipe.time_created,
                reverse=True)
        context = {"titre": titre, 'recipes': recipes}
    else:
        message = "Tu n'as pas encore publié de recette"
        context = {"titre": titre, "message": message, 'recipes': recipes}
    return render(request, 'recipes/my_recipes.html', context)

@login_required(login_url='connexion')
def createRecipe(request):
    title = 'Décris nous ta recette:'
    if request.method == 'POST':
        form = CreateRecipe(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user
            recipe.save()
            recipe_title = form.cleaned_data.get('title')
            messages.success(request, 'Ta recette: ' + recipe_title +  ' a bien été créée')
            return redirect('recipes')
    else:
        form = CreateRecipe()
    context = {'form': form, 'title':title}
    return render(request, 'recipes/create_recipe_view.html', context)

@login_required(login_url='connexion')
def deleteRecipe(request, recipe_id=int):
    if request.method == 'GET':
        recipe = Recipe.objects.get(id__exact=recipe_id)
        recipe.delete()
        messages.success(request, 'Ta recette a bien été supprimée')
        return redirect('recipes')
    return render(request, 'recipes/my_recipes.html')

@login_required(login_url='connexion')
def modifyRecipe(request, recipe_id=int):
    context={}
    recipe = Recipe.objects.get(id__exact=recipe_id)
    if request.method == 'GET':
        form = CreateRecipe(instance=recipe)
        context = {'form': form}
    if request.method == 'POST':
        form = CreateRecipe(request.POST, request.FILES)
        if form.is_valid():
            recipe.title = form.cleaned_data['title']
            recipe.ingredients = form.cleaned_data['ingredients']
            recipe.description = form.cleaned_data['description']
            if form.cleaned_data['image'] is False:
                recipe.image = None
            elif form.cleaned_data['image'] is not None:
                recipe.image = form.cleaned_data['image']
            if form.cleaned_data['recipe_tag'] is False:
                recipe.recipe_tag = None
            elif form.cleaned_data['recipe_tag'] is not None:
                recipe.recipe_tag = form.cleaned_data['recipe_tag']
            recipe.save()
            messages.success(request, 'ta recette "' + recipe.title +'" a bien été modifiée')
        return redirect('recipes')
    return render(request, 'recipes/create_recipe_view.html', context)
