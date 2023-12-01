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


class TestUrls(TestSetUp):
    """
    class to check that urls are accessing and associated templates well returned
    """
    def test_recipes_index_view(self):
        """
        Unitary test for home page, check recipes_index() method is called on url '/'
        """
        found = resolve("/")
        self.assertEqual(found.func, recipes_index)

    def test_recipes_index(self):
        """
        Unitary test for home page,
        check well acces on url '/' and recipes template is returned
        """
        response = self.client.get("/")
        assert response.status_code == 200
        assert b"Bienvenue sur notre forum culinaire" in response.content

    def test_detail_recipe_view(self):
        """
        Unitary test for detail recipe view,
        check well acces on url 'detail_recipe/' and detail_recipes template is returned
        """
        response = self.client.get("/detail_recipe/"+ str(self.recipe1.id) + "/")
        assert response.status_code == 200
        assert b'<h3 class="d-flex justify-content-center">title recipe1</h3>\n' in response.content
        assert b'Note moyenne: 3.0/5' in response.content


    def test_get_my_recipes(self):
        """
        Unitary test for my_recipes page,
        check well acces on url '/my_recipes/' and my_recipes/index template is returned
        """
        self.client.force_login(self.user1)
        response = self.client.get("/my_recipes")
        print ("response.status_code", response.status_code)
        assert response.status_code == 200
        expected = f'<h3>{self.recipe1.title}</h3>'
        assert (
            expected
            in response.content.decode()
        )
        assert (
            b'Bienvenue sur ta page de recettes'
            in response.content
        )

    def test_get_forbidden_views_without_login(self):
        """
        Unitary test for all pages where login required
        """
        response = self.client.get("/my_recipes")
        assert response.status_code == 302
        assert response['Location'] == "/users/connexion/?next=/my_recipes"

    def test_wrong_url(self):
        response = self.client.get("/WrongUrl")
        expected_html = render_to_string("404.html")
        self.assertEqual(
            response.content.decode(),
            expected_html,
        )
        assert (
            b"Retourner sur la page de recette avec le lien ci-dessous"
            in response.content
        )

    def test_wrong_recipe(self):
        response = self.client.get("/detail_recipe/50/")
        expected_html = render_to_string("404.html")
        self.assertEqual(
            response.content.decode(),
            expected_html,
        )
        assert (
            b"Retourner sur la page de recette avec le lien ci-dessous"
            in response.content
        )
