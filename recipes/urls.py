from django.urls import path
from . import views

urlpatterns = [
    path('', views.recipes_index, name='recipes'),
    path('my_recipes', views.my_recipes, name='my_recipes'),
    path('create_recipe', views.createRecipe, name='create_recipe'),
    path('delete_recipe/<int:recipe_id>/', views.deleteRecipe, name='delete_recipe'),
    path('modify_recipe/<int:recipe_id>/', views.modifyRecipe, name='modify_recipe')
    ]