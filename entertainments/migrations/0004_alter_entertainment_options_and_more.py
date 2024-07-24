# Generated by Django 5.0.7 on 2024-07-17 13:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entertainments', '0003_entertainment_images'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='entertainment',
            options={'verbose_name': 'Достопримечательность', 'verbose_name_plural': 'Достопримечательности'},
        ),
        migrations.RemoveField(
            model_name='entertainment',
            name='images',
        ),
        migrations.CreateModel(
            name='EntertainmentImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
                ('entertainment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='entertainments.entertainment')),
            ],
        ),
    ]
