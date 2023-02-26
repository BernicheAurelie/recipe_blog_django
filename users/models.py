import django.contrib.auth.models
from django.db import models


class User(models.Model):
    user = django.contrib.auth.models.User
