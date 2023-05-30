# Generated by Django 4.1.7 on 2023-02-24 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0005_alter_recipe_recipe_tag_delete_recipetag"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recipe",
            name="recipe_tag",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Apéritif", "Apéritif"),
                    ("Plat", "Plat"),
                    ("Accompagnement", "Accompagnement"),
                    ("Dessert", "Dessert"),
                    ("Sauce", "Sauce"),
                    ("Autre", "autre"),
                ],
                default="Autre",
                max_length=25,
                null=True,
            ),
        ),
    ]
