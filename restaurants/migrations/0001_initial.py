# Generated by Django 5.0.7 on 2024-09-19 09:13

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Restaurant",
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
            ],
            options={
                "verbose_name": "Объект питания",
                "verbose_name_plural": "Объекты питания",
            },
        ),
        migrations.CreateModel(
            name="RestaurantImage",
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
            ],
        ),
    ]
