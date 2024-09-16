# Generated by Django 5.0.7 on 2024-09-16 13:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="BodyType",
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
                (
                    "name",
                    models.CharField(
                        blank=True, max_length=100, null=True, verbose_name="Тип кузова"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Brand",
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
                (
                    "name",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        null=True,
                        verbose_name="Бренд машины",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Color",
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
                (
                    "name",
                    models.CharField(
                        blank=True, max_length=50, null=True, verbose_name="Цвет машины"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Model",
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
                (
                    "name",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        null=True,
                        verbose_name="Модель машины",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Year",
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
                (
                    "name",
                    models.PositiveIntegerField(
                        blank=True, null=True, verbose_name="Год выпуска машины"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Auto",
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
                (
                    "body_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="kashiring.bodytype",
                        verbose_name="Кузов",
                    ),
                ),
                (
                    "brand",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="kashiring.brand",
                        verbose_name="Брэнд",
                    ),
                ),
                (
                    "color",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="kashiring.color",
                        verbose_name="Цвет",
                    ),
                ),
                (
                    "model",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="kashiring.model",
                        verbose_name="Модель",
                    ),
                ),
                (
                    "year",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="kashiring.year",
                        verbose_name="Год выпуска",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Company",
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
                ("working_hours", models.TextField(blank=True, null=True)),
                (
                    "auto",
                    models.ManyToManyField(
                        blank=True, to="kashiring.auto", verbose_name="машины"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Foto",
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
                (
                    "image",
                    models.ImageField(
                        blank=True, null=True, upload_to="content_images/"
                    ),
                ),
                (
                    "auto",
                    models.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="Машина",
                        to="kashiring.auto",
                    ),
                ),
            ],
        ),
    ]
