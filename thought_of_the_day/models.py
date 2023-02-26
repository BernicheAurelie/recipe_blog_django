from django.db import models

# Create your models here.
class Thought(models.Model):
    thought = models.TextField(max_length=8192, blank=True)