# Generated by Django 4.1.7 on 2023-03-06 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("comments", "0004_remove_comment_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="last_updated",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name="comment",
            name="time_created",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]