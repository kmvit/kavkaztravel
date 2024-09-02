from django.db import models
from core.models import BaseContent


class Company(BaseContent):
    """Класс для модели Компа."""
    working_hours = models.TextField(blank=True, null=True)
    auto = models.ManyToManyField("Компании", blank=True, verbose_name="машины")


class Auto(BaseContent):
    """Класс для модели Машины."""
    brand = models.CharField(max_length=100, verbose_name="Бренд машины", blank=True, null=True)
    model = models.CharField(max_length=100, verbose_name="Модель машины", blank=True, null=True)
    year = models.PositiveIntegerField(verbose_name="Год выпуска машины", blank=True, null=True)
    color = models.CharField(max_length=50, verbose_name="Цвет машины", blank=True, null=True)
    body_type = models.CharField(max_length=100, verbose_name="Тип кузова", blank=True, null=True)

    def __str__(self):
        return self.model

class Foto(models.Model):
    """Класс для модели фото машины."""
    image = models.ImageField(upload_to='content_images/', blank=True,
                              null=True)
    auto = models.ForeignKey(
       Auto, on_delete=models.CASCADE, related_name="Фото машины", blank=True
    )
