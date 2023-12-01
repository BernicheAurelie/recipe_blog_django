from django.test import TestCase
import django
import os


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

django.setup()

from recipes.models import Recipe
from comments.models import Comment
from users.models import User


class TestSetUp(TestCase):
    def setUp(self):
        """
        Set up method to initialize database
        for recipes and comments unitaries tests
        """
        self.user1 = User.objects.create(
            username="username1",
            email="username1@test.com",
            password="test1234",
        )
        self.user2 = User.objects.create(
            username="username2",
            email="username2@test.com",
            password="test1234",
        )
        self.user3 = User.objects.create(
            username="username3",
            email="username3@test.com",
            password="test1234",
        )
        self.recipe1 = Recipe.objects.create(
            user=self.user1,
            title="title recipe1",
            ingredients="ingredients recipe1",
            description="description recipe1",
        )
        self.recipe2 = Recipe.objects.create(
            user=self.user2,
            title="title recipe2",
            ingredients="ingredients recipe2",
            description="description recipe2",
        )
        self.comment1 = Comment.objects.create(
            user=self.user1,
            recipe=self.recipe1,
            title="title comment1",
            description="description comment1",
            rating=3,
        )
        self.comment2 = Comment.objects.create(
            user=self.user2,
            recipe=self.recipe2,
            title="title comment2",
            description="description comment2",
            rating=3,
        )
