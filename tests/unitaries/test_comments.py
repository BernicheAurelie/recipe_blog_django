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



class TestComment(TestSetUp):
    def test_get_comment_need_authentification(self):
        response = self.client.get("/comments/")
        assert response.status_code == 302
        assert response['Location'] == "/users/connexion/?next=/comments/"

    def test_get_user_comments(self):
        """
        check user can get all comment comment1 and comment2 in setup
        """
        self.client.force_login(self.user1)
        response = self.client.get("/comments/")
        assert b"Bienvenue sur tes commentaires" in response.content
        assert b"<h6>Titre: title comment1</h6>\n" in response.content

    def test_get_all_comments_for_a_recipe(self):
        """
        check user can get a comment with my_comments_view
        """
        self.client.force_login(self.user2)
        url = "/comments/associated_comments/" + str(self.recipe1.id) + '/'
        response = self.client.get(url)
        assert b'title comment1' in response.content
        assert b'title comment2' not in response.content
        assert b'description comment1' in response.content
        
    def test_create_comment_authentification_required(self):
        url = "/comments/create/" + str(self.recipe1.id) + "/"
        response = self.client.get(url)
        assert response.status_code == 302
        assert response['Location'] == f"/users/connexion/?next={url}"

    def test_create_and_modify_comment(self):
        self.client.force_login(self.user1)
        url = "/comments/create/" + str(self.recipe1.id) + "/"
        response = self.client.post(url, data={
            'title':"title test comment",
            'description':"description test comment",
            'rating':5,
        })
        assert response.status_code == 302
        assert response['Location'] == "/"
        response2 = self.client.get("/comments/")
        assert b'ton commentaire a bien \xc3\xa9t\xc3\xa9 cr\xc3\xa9\xc3\xa9' in response2.content
        assert b'title test comment' in response2.content
        response3 = self.client.post(url, data={
            'title':"modification title test comment",
            'description':"modification description test comment",
            'rating':0,
        })
        response4 = self.client.get("/comments/")
        assert b'modification title test comment' in response4.content

    def test_modify_or_delete_comment_only_allowed_to_author(self):
        self.client.force_login(self.user2)
        url = '/comments/modify_comment/' + str(self.comment1.id) + '/'
        response = self.client.post(url, data={
            'title':"modification title test comment",
            'description':"modification description test comment",
            'rating':0,
        })
        assert response.status_code==302
        assert response['Location'] == "/comments/"
        response2 = self.client.get("/comments/")
        assert b'modification title test comment' not in response2.content
        url2 = "/comments/delete_comment/" + str(self.comment1.id) + '/'
        response3 = self.client.post(url2)
        assert response3.status_code==302
        assert response3['Location'] == "/comments/"
        self.client.force_login(self.user1)
        response4 = self.client.post(url2)
        verification = self.client.get("/comments/")
        assert b'title comment1' not in verification.content

    def test_delete_comment_forbidden(self):
        self.client.force_login(self.user2)
        url = "/comments/delete_comment/" + str(self.comment1.id) + '/'
        response = self.client.post(url)
        assert response.status_code == 302
        assert response['Location'] == "/comments/"
        url2 = "/comments/associated_comments/" + str(self.comment1.recipe.id) + '/'
        verification = self.client.get(url2)
        title = self.comment1.title
        res = bytes(title, "utf-8")
        assert res in verification.content
