# Generated by Django 5.0.7 on 2024-07-24 06:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0005_alter_hotel_options_remove_hotel_images_hotelimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccommodationType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Amenity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MealPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('capacity', models.IntegerField()),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to='hotels.hotel')),
            ],
        ),
        migrations.CreateModel(
            name='RoomImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='room_images/')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='hotels.room')),
            ],
        ),
        migrations.CreateModel(
            name='RoomPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('season', models.CharField(choices=[('low', 'Low Season'), ('high', 'High Season'), ('holiday', 'Holiday Season')], default='low', max_length=10)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prices', to='hotels.room')),
            ],
            options={
                'unique_together': {('room', 'date')},
            },
        ),
    ]
