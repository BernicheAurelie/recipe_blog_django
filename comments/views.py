from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from recipes.models import Recipe
from comments.forms import CreateComments
from comments.models import Comment

def comments_index(request):
    title = "Bienvenue sur les commentaires" 
    comments = Comment.objects.all()
    context = {"title": title, "comments": comments}
    return render(request,"comments/comments.html", context)

@login_required(login_url='connexion')
def createComment(request, recipe_id=None):
    recipe = Recipe.objects.get(id__exact=recipe_id)
    title = f'Commenter la recette: {recipe.title}'
    if request.method == 'POST' and recipe_id is not None:
        form = CreateComments(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.recipe = recipe
            recipe.commented = True
            recipe.save()
            comment.save()
            messages.success(request, 'ton commentaire a bien été créé')
            return redirect('recipes')
    else:
        form = CreateComments()
    context = {'form': form, "title":title, "recipe":recipe}
    return render(request, "comments/create_comments.html", context)

def deleteComment(request, comment_id):
    ...

def modifyComment(request, comment_id):
    ...