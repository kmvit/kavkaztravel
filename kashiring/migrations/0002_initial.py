# Generated by Django 5.0.7 on 2024-09-17 07:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("kashiring", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="company",
            name="owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="company",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="foto",
            name="auto",
            field=models.ForeignKey(
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="Машина",
                to="kashiring.auto",
            ),
        ),
        migrations.AddField(
            model_name="auto",
            name="model",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="kashiring.model",
                verbose_name="Модель",
            ),
        ),
        migrations.AddField(
            model_name="auto",
            name="year",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="kashiring.year",
                verbose_name="Год выпуска",
            ),
        ),
    ]
