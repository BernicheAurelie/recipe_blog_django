# Generated by Django 4.1.7 on 2023-03-05 07:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("comments", "0003_rename_body_comment_description_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="comment",
            name="image",
        ),
    ]
