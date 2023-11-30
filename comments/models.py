from django.db import models
from django.conf import settings
from recipes.models import Recipe
from django.core.validators import MinValueValidator, MaxValueValidator


class Comment(models.Model):
    recipe = models.ForeignKey(to=Recipe, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=1000, blank=True)    
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title