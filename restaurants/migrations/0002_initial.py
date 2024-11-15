# Generated by Django 5.0.7 on 2024-11-15 16:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("regions", "0002_initial"),
        ("restaurants", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="restaurant",
            name="owner",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="restaurants",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="restaurant",
            name="region",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="restaurants",
                to="regions.region",
            ),
        ),
        migrations.AddField(
            model_name="restaurantimage",
            name="restaurant",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="images",
                to="restaurants.restaurant",
            ),
        ),
        migrations.AddField(
            model_name="reviewrestaurant",
            name="owner",
            field=models.ForeignKey(
                default=1,
                help_text="Пользователь, оставивший отзыв.",
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Владелец отзыва",
            ),
        ),
        migrations.AddField(
            model_name="reviewrestaurant",
            name="restaurant",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="restaurant",
                to="restaurants.restaurant",
                verbose_name="Место общественного питания",
            ),
        ),
    ]
