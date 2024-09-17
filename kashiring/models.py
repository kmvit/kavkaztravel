from django.conf import settings
from django.db import models
from core.models import BaseContent


class Brand(BaseContent):
    """Класс для брэнда машины."""
    name = models.CharField(max_length=100, verbose_name="Бренд машины", blank=True, null=True)

    def __str__(self):
        return self.name

class Model(BaseContent):
    """Класс для модели машины."""
    name = models.CharField(max_length=100, verbose_name="Модель машины", blank=True, null=True)

    def __str__(self):
        return self.name


class Year(BaseContent):
    """Класс для года выпуска машины."""
    name = models.PositiveIntegerField(verbose_name="Год выпуска машины", blank=True, null=True)

 

class Color(BaseContent):
    """Класс для года выпуска машины."""
    name = models.CharField(max_length=50, verbose_name="Цвет машины", blank=True, null=True)
    
    def __str__(self):
        return self.name


class BodyType(BaseContent):
    """Класс для типа кузова машины."""
    name = models.CharField(max_length=100, verbose_name="Тип кузова", blank=True, null=True)

    def __str__(self):
        return self.name


class Auto(BaseContent):
    """Класс для модели Машины."""
    brand = models.ForeignKey(Brand,
        on_delete=models.CASCADE, null=True,
                               blank=True,
    )
    model = models.ForeignKey(Model,
        on_delete=models.CASCADE, null=True,
                               blank=True,
    )
    year = models.ForeignKey(Year,
        on_delete=models.CASCADE, null=True,
                               blank=True,
    )
    color = models.ForeignKey(Color,
        on_delete=models.CASCADE, null=True,
                               blank=True,
    )
    body_type = models.ForeignKey(BodyType,
        on_delete=models.CASCADE, null=True,
                               blank=True,
    )

    def __str__(self):
      return str(self.name)
    

class Foto(models.Model):
    """Класс для модели фото машины."""
    image = models.ImageField(upload_to='content_images/', blank=True,
                              null=True)
    auto = models.ForeignKey(
       Auto, on_delete=models.CASCADE, related_name="Машина", blank=True
    )

class Company(BaseContent):
    """Класс для модели Компа."""
    working_hours = models.TextField(blank=True, null=True)
    auto = models.ManyToManyField(Auto, blank=True, verbose_name="машины")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,
                              related_name='company')
    
