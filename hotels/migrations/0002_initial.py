# Generated by Django 5.0.7 on 2024-10-21 10:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("hotels", "0001_initial"),
        ("regions", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="hotel",
            name="owner",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="hotels",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="hotel",
            name="region",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="hotels",
                to="regions.region",
            ),
        ),
        migrations.AddField(
            model_name="hotelimage",
            name="hotel",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="images",
                to="hotels.hotel",
            ),
        ),
        migrations.AddField(
            model_name="room",
            name="hotel",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="rooms",
                to="hotels.hotel",
            ),
        ),
        migrations.AddField(
            model_name="room",
            name="owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="room",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="roomimage",
            name="room",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="images",
                to="hotels.room",
            ),
        ),
        migrations.AddField(
            model_name="roomprice",
            name="room",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="prices",
                to="hotels.room",
            ),
        ),
        migrations.AddField(
            model_name="hotel",
            name="tags",
            field=models.ManyToManyField(related_name="hotels", to="hotels.tag"),
        ),
        migrations.AlterUniqueTogether(
            name="roomprice",
            unique_together={("room", "date")},
        ),
    ]
