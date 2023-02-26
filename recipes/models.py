from django.db import models
from django.conf import settings


class Recipe(models.Model):
    title = models.CharField(max_length=128, null=True)
    description = models.TextField(max_length=2048, blank=True, null=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    STARTER = 'Apéritif'
    MEAL = 'Plat'
    TRIMMING = 'Accompagnement'
    PUDDING = 'Dessert'
    DIP = 'Sauce'
    OTHER = 'Autre'

    CHOICES = [(STARTER, ('Apéritif')), (MEAL, ('Plat')), (TRIMMING, ('Accompagnement')), 
            (PUDDING, ('Dessert')), (DIP, ('Sauce')), (OTHER,('autre'))
            ]
    recipe_tag = models.CharField(max_length=25, choices=CHOICES, default=OTHER, blank=True, null=True)
    time_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    commented = models.BooleanField(default=False)

    def __str__(self):
        return self.title


# class RecipeTag(models.Model):
#     STARTER = 'Apéritif'
#     MEAL = 'Plat'
#     TRIMMING = 'Accompagnement'
#     PUDDING = 'Dessert'
#     DIP = 'Sauce'
#     OTHER = 'Autre'

#     CHOICES = [(STARTER, ('Apéritif')), (MEAL, ('Plat')), (TRIMMING, ('Accompagnement')), 
#             (TRIMMING, ('Accompagnement')), (PUDDING, ('Dessert')), (DIP, ('Sauce')), (OTHER,('autre'))
#             ]
#     tag = models.CharField(max_length=20, choices=CHOICES, default=OTHER)

#     def __str__(self):
#         return f"{self.tag}"

#     class Meta:
#         verbose_name = 'Catégorie'
#         verbose_name_plural = 'Catégories'