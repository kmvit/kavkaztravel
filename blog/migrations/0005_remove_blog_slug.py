# Generated by Django 5.0.7 on 2024-08-29 13:06

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0004_alter_blog_content"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="blog",
            name="slug",
        ),
    ]
