import pytest
import django
from django.test import TestCase
from django.template.loader import render_to_string
from django.urls import resolve
import os


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

django.setup()

from tests.test_setup import TestSetUp
from recipes.views import recipes_index, detail_recipe_view, my_recipes, modifyRecipe, createRecipe, deleteRecipe
from comments.views import associated_comments, my_comments, createComment, deleteComment, modifyComment



class TestRecipes(TestSetUp):
    def test_get_all_recipes(self):
        """
        check user can get all recipe recipe1 and recipe2 in setup
        """
        response = self.client.get("/")
        print(response.content)
        assert b"title recipe1\n" in response.content
        assert b"title recipe2\n" in response.content

    def test_get_a_recipe(self):
        """
        check user can get a recipe with detail_recipe_view
        """
        response = self.client.get("/detail_recipe/4/")
        assert b"4e recette" in response.content
        
    def test_create_recipe_authentification_required(self):
        response = self.client.post(
            "/create_recipe", 
            data={
            "title":"title test recipe",
            "ingredients":"ingredients test recipe",
            "description":"description test recipe",
            }
        )
        assert response.status_code == 302
        assert response['Location'] == "/users/connexion/?next=/create_recipe"

    def test_create_recipe(self):
        self.client.force_login(self.user1)
        response = self.client.post(
            "/create_recipe", 
            data={
            "title":"title test recipe",
            "ingredients":"ingredients test recipe",
            "description":"description test recipe",
            }
        )
        assert response.status_code == 302
        response2 = self.client.get('/my_recipes')
        assert b"Bienvenue sur ta page de recettes" in response2.content
        assert b'Ta recette: title test recipe a bien \xc3\xa9t\xc3\xa9 cr\xc3\xa9\xc3\xa9e' in response2.content
        assert b'<h3>title test recipe</h3>\n' in response2.content  

    def test_modify_a_recipe_forbidden(self):
        """
        check user can't neither modify nor delete a recipe
        if he isn't recipes's author
        """
        response = self.client.get("/modify_recipe/4/")
        assert response.status_code == 302
        assert response['Location'] == "/users/connexion/?next=/modify_recipe/4/"
        self.client.force_login(self.user1)
        response = self.client.get("/modify_recipe/4/")
        response1 = self.client.post(
            "/modify_recipe/4/",
            data={
                "title": "titre modifié de la recette 4",
                "ingredients": "ingrédients modifiés de la recette 4",
                "description": "description modifiée de la recette 4",
            },
        )
        assert response1.status_code == 302
        assert response['Location'] == "/"

    def test_delete_a_recipe_forbidden(self):
        """
        check user can't neither modify nor delete a recipe
        if he isn't recipes's author
        """
        response = self.client.get("/delete_recipe/4/")
        assert response.status_code == 302
        assert response['Location'] == "/users/connexion/?next=/delete_recipe/4/"
        self.client.force_login(self.user1)
        response1 = self.client.get("/delete_recipe/4/")
        print("try get delete: response.status_code: ", response1.status_code)
        response2 = self.client.post(
            "/delete_recipe/4/"
        )
        print("response2['Location']: ", response2['Location'])
        assert response2.status_code == 302
        assert response2['Location'] == "/"
        final_response = self.client.get("/")
        assert b'Cette recette ne peut \xc3\xaatre supprim\xc3\xa9e que par son auteur' in final_response.content
        verification = self.client.get("/detail_recipe/4/")
        assert b'4e recette' in verification.content
    
    
    
    def test_modify_a_recipe(self):
        """
        check user can modify a recipe with modify_recipe_view
        if user is authenticated and is recipes's author
        """
        self.client.force_login(self.user1)
        url = "/modify_recipe/" + str(self.recipe1.id) + "/"
        response = self.client.get(url)
        response1 = self.client.post(
            url,
            data={
                "title": "modification title recipe1",
                "ingredients": "modification ingredients recipe1",
                "description": "modification description recipe1",
            },
        )
        url2 = "/detail_recipe/" + str(self.recipe1.id) + "/"
        response2 = self.client.get(url2)
        print("response2.content: ", response2.content)
        assert b'modification title recipe1' in response2.content

    def test_delete_a_recipe(self):
        """
        check user can delete a recipe with delete_recipe_view
        if user is authenticated and is recipes's author
        """
        self.client.force_login(self.user1)
        url = "/delete_recipe/" + str(self.recipe1.id) + "/"
        response = self.client.get(url)
        response1 = self.client.post(url)
        url2 = "/detail_recipe/" + str(self.recipe1.id) + "/"
        response2 = self.client.get(url2)
        assert b'Ta recette a bien \xc3\xa9t\xc3\xa9 supprim\xc3\xa9e' in response2.content
        assert b'Une erreur est apparue' in response2.content
        assert b'Retourner sur la page de recette avec le lien ci-dessous' in response2.content
