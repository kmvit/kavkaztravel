# Generated by Django 5.0.7 on 2024-08-28 11:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="blog",
            name="slug",
            field=models.SlugField(
                default=1, max_length=255, unique=True, verbose_name="URL"
            ),
            preserve_default=False,
        ),
    ]
