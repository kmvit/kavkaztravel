# Generated by Django 5.0.7 on 2024-09-16 13:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("regions", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Entertainment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("url", models.SlugField(blank=True, unique=True)),
                ("description", models.TextField(blank=True, null=True)),
                ("date", models.DateField(auto_now_add=True, null=True)),
                ("content", models.TextField(blank=True, null=True)),
                (
                    "image",
                    models.ImageField(
                        blank=True, null=True, upload_to="content_images/"
                    ),
                ),
                ("seo_title", models.CharField(blank=True, max_length=255, null=True)),
                ("seo_description", models.TextField(blank=True, null=True)),
                ("address", models.CharField(max_length=300)),
                (
                    "region",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="entertainments",
                        to="regions.region",
                    ),
                ),
            ],
            options={
                "verbose_name": "Достопримечательность",
                "verbose_name_plural": "Достопримечательности",
            },
        ),
        migrations.CreateModel(
            name="EntertainmentImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("image", models.ImageField(upload_to="")),
                (
                    "entertainment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="entertainments.entertainment",
                    ),
                ),
            ],
        ),
    ]
