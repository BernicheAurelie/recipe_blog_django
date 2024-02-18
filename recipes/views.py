from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.db.models import CharField, Value, Q, Count, Avg, Min, Max
from django.db.models.functions import Length
from django.utils.html import strip_tags
import datetime
from comments.models import Comment
from .forms import CreateRecipe
from .models import Recipe
from utils import logger


def search_view(request):
    comments=[]
    today = datetime.date.today()
    titre = "Bienvenue sur notre forum culinaire"

    if request.method == "GET":
        name = request.GET.get("recherche")
        name = strip_tags(name)
        if name is not None:
            recipes = Recipe.objects.annotate(num_comments=Count("comment")).filter(
                Q(title__icontains=name)|
                Q(ingredients__icontains=name)|
                Q(description__icontains=name)|
                Q(recipe_tag=name)
                )
            if not recipes:
                titre = "Il n'y a pas encore de recette correspondant à la recherche."
                context = {"titre": titre}
                return render(request, 'recipes/recipes.html', context)
            else:
                len_recipes = len(recipes)
                if len_recipes>=2:
                    titre = f"Il y a {len_recipes} recettes correspondant à la recherche."
                elif len_recipes == 1:
                    titre = f"Il y a {len_recipes} recette correspondant à la recherche."
                # get three first associated comments:
                for recipe in recipes:
                    associated_comments = Comment.objects.filter(recipe_id=recipe.id)
                    comments.extend(associated_comments[:3])
                    recipe.time_created.strftime('%d-%m-%Y')
                    recipe.last_updated.strftime('%d-%m-%Y')
                posts = sorted(recipes,
                        key=lambda post: post.time_created,
                        reverse=True
                    )
                comments = sorted(comments,
                        key=lambda comment: comment.time_created,
                        reverse=True
                    )
                context = {"titre": titre, 'posts': posts, 'comments': comments, 'today': today}
                return render(request, 'recipes/recipes.html', context)

def recipes_index(request):
    titre = "Bienvenue sur notre forum culinaire"
    today = datetime.date.today()
    # recipes = Recipe.objects.select_related("user").all()
    recipes = Recipe.objects.select_related("user").annotate(
        num_comments=Count("comment")
        ).annotate(
            avg_rating=Avg("comment__rating")
            ).annotate(
                len_title=Length("title")
                )      
    comments=[]
    # get three first associated comments:
    for recipe in recipes:
        associated_comments = Comment.objects.filter(recipe_id=recipe.id)
        comments.extend(associated_comments[:3])
        recipe.time_created.strftime('%d-%m-%Y')
        recipe.last_updated.strftime('%d-%m-%Y')
    posts = sorted(recipes,
            key=lambda post: post.time_created,
            reverse=True
        )
    comments = sorted(comments,
            key=lambda comment: comment.time_created,
            reverse=True
        )
    context = {"titre": titre, 'posts': posts, 'comments': comments, 'today': today}
    return render(request, 'recipes/recipes.html', context)

def detail_recipe_view(request, recipe_id=int):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    recipe.time_created.strftime('%d-%m-%Y')
    recipe.last_updated.strftime('%d-%m-%Y')
    comments = Comment.objects.filter(recipe_id=recipe.id)
    len_comments=len(comments)
    rating = 0
    try:
        for comment in comments:
            rating += comment.rating
        avg_rating = rating/len_comments
    except ZeroDivisionError:
        avg_rating = 0
    if len_comments>0:
        title=f'Note moyenne: {avg_rating}/5'
    else:
        title="Cette recette n'est pas encore notée"
    context = {'recipe': recipe, "comments":comments, "avg_rating":avg_rating, "title":title, "len_comments":len_comments}
    return render(request, 'recipes/detail_recipe.html', context)

@login_required(login_url='connexion')
def my_recipes(request):
    titre = "Bienvenue sur ta page de recettes"
    context = {"titre": titre}
    user = request.user
    recipes = Recipe.objects.filter(
        user__exact=user
        ).annotate(
            num_comments=Count("comment")
            ).annotate(
                avg_rating=Avg("comment__rating")
                ).annotate(
                    len_title=Length("title")
                    )

    for recipe in recipes:
        recipe.time_created.strftime('%d-%m-%Y')
        recipe.last_updated.strftime('%d-%m-%Y')

    if recipes:
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
def modifyRecipe(request, recipe_id=int):
    context={}
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user.id == recipe.user.id:
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
                messages.success(request, 'Ta recette "' + recipe.title +'" a bien été modifiée')
            return redirect('recipes')
    else:
        messages.error(request, 'Cette recette ne peut être modifiée que par son auteur')
        return redirect('recipes')
    return render(request, 'recipes/create_recipe_view.html', context)

@login_required(login_url='connexion')
def deleteRecipe(request, recipe_id=int):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    context = {"recipe": recipe}
    if request.user.id == recipe.user.id:
        if request.method == 'POST':
            recipe.delete()
            messages.success(request, 'Ta recette a bien été supprimée')
            return redirect('recipes')
    else:
        messages.error(request, 'Cette recette ne peut être supprimée que par son auteur')
        return redirect('recipes')
    return render(request, 'recipes/delete_recipe.html', context)
