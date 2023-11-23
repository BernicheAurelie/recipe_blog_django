from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """ Custom user"""
    username = models.CharField(max_length=50,)
    password1 = models.CharField(max_length=50)
    password2 = models.CharField(max_length=50)
    email = models.EmailField(max_length=88, unique=True)

    def __str__(self):
        return self.username

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']