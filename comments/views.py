from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from recipes.models import Recipe
from comments.forms import CreateComments
from comments.models import Comment


@login_required(login_url='connexion')
def my_comments(request):
    title = "Bienvenue sur tes commentaires" 
    comments = Comment.objects.filter(user=request.user)
    context = {"title": title, "comments": comments}
    return render(request,"comments/my_comments.html", context)

@login_required(login_url='connexion')
def associated_comments(request, recipe_id):
    # recipe = Recipe.objects.get(id=recipe_id)
    recipe = get_object_or_404(Recipe, id=recipe_id)
    title = f'Commentaires associés à la recette: "{recipe.title}"' 
    comments = Comment.objects.filter(recipe_id=recipe_id)
    len_comments=len(comments)
    rating = 0
    try:
        for comment in comments:
            rating += comment.rating
        avg_rating = rating/len_comments
    except ZeroDivisionError:
        avg_rating = 0
    note_moyenne = f'Note moyenne: {avg_rating}/5'
    context = {"title": title, "comments": comments, "avg_rating":avg_rating, 'note_moyenne':note_moyenne, "recipe":recipe, "len_comments":len_comments}
    return render(request,"comments/associated_comments.html", context)

@login_required(login_url='connexion')
def createComment(request, recipe_id=None):
    # recipe = Recipe.objects.get(id__exact=recipe_id)
    recipe = get_object_or_404(Recipe, id=recipe_id)
    title = str(recipe.title)
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

@login_required(login_url='connexion')
def deleteComment(request, comment_id=int):
    # comment = Comment.objects.get(id=comment_id)
    comment = get_object_or_404(Comment, id=comment_id)
    print("request.user.id == ", request.user.id)
    print("comment.user.id == ", comment.user.id)
    if request.user.id == comment.user.id:
        context = {"comment":comment}
        if request.method == 'POST':
            comment.delete()
            messages.success(request, "Ton commentaire a bien été supprimé")
            return redirect("my_comments")
    else:
        messages.error(request, "Ce commentaire ne peut être supprimé que par son auteur")
        return redirect("my_comments")
    return render(request, "comments/delete_comment.html", context) 

# @login_required(login_url='connexion')
# def deleteComment(request, comment_id=int):
#     if request.method == 'GET':
#         comment = Comment.objects.get(id=comment_id)
#         comment.delete()
#         messages.success(request, "Ton commentaire a bien été supprimé")
#         return redirect("my_comments")
#     return render("comments/my_comments.html")    

@login_required(login_url='connexion')
def modifyComment(request, comment_id=int):
    context={}
    # comment = Comment.objects.get(id=comment_id)
    comment = get_object_or_404(Comment, id=comment_id)
    print("request.user.id == ", request.user.id)
    print("comment.user.id == ", comment.user.id)
    if request.user.id == comment.user.id:
        if request.method == 'GET':
            form = CreateComments(instance=comment)
            context = {'form': form}
        if request.method == 'POST':
            form = CreateComments(request.POST, request.FILES)
            if form.is_valid():
                comment.title = form.cleaned_data['title']
                comment.description = form.cleaned_data['description']
                comment.rating = form.cleaned_data['rating']
                comment.save()
                messages.success(request, 'ton commentaire "' + comment.title +'" a bien été modifié')
            return redirect('my_comments')
    else:
        messages.error(request, 'Ce commentaire ne peut être modifié que par son auteur')
        return redirect('my_comments')
    return render(request, "comments/create_comments.html", context)
