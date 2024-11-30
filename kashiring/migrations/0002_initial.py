# Generated by Django 5.0.7 on 2024-11-30 05:14

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
            model_name="auto",
            name="owner",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="auto",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="auto",
            name="body_type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="kashiring.bodytype",
            ),
        ),
        migrations.AddField(
            model_name="auto",
            name="brand",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="kashiring.brand",
            ),
        ),
        migrations.AddField(
            model_name="auto",
            name="color",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="kashiring.color",
            ),
        ),
        migrations.AddField(
            model_name="company",
            name="auto",
            field=models.ManyToManyField(
                blank=True, to="kashiring.auto", verbose_name="машины"
            ),
        ),
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
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="kashiring.model",
            ),
        ),
        migrations.AddField(
            model_name="auto",
            name="year",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="kashiring.year",
            ),
        ),
    ]
