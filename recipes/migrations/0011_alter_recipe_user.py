# Generated by Django 4.2.7 on 2023-11-20 10:22

from django.conf import settings
from django.db import migrations, models
import recipes.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("recipes", "0010_alter_recipe_title"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recipe",
            name="user",
            field=models.ForeignKey(
                on_delete=models.SET(recipes.models.get_sentinel_user),
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
