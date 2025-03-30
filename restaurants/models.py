from django.db import models
from django.conf import settings
from regions.models import Region


class RestaurantType(models.Model):
    name = models.CharField("Название", max_length=100, unique=True)
    description = models.TextField("Описание", blank=True, null=True)

    class Meta:
        verbose_name = "Тип ресторана"
        verbose_name_plural = "Типы ресторанов"

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField("Название", max_length=100, unique=True)
    description = models.TextField("Описание", blank=True, null=True)

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    address = models.CharField("Адрес", max_length=300)
    name = models.CharField("Название", max_length=300)
    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        related_name="restaurants",
        verbose_name="Регион",
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="restaurants",
        verbose_name="Владелец",
    )
    average_check = models.DecimalField(
        "Средний чек", max_digits=10, decimal_places=2, null=True, blank=True
    )
    description = models.TextField("Описание", blank=True, null=True)
    restaurant_type = models.ForeignKey(
        RestaurantType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="restaurants",
        verbose_name="Тип ресторана",
    )
    working_hours = models.CharField(
        "Часы работы", max_length=100, blank=True, null=True
    )  # Часы работы ресторана
    services = models.ManyToManyField(
        Service, blank=True, related_name="restaurants", verbose_name="Услуги"
    )

    class Meta:
        verbose_name = "Ресторан"
        verbose_name_plural = "Рестораны"

    def __str__(self):
        return self.name


class RestaurantImage(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name="images",
        on_delete=models.CASCADE,
        verbose_name="Ресторан",
    )
    image = models.ImageField("Изображение")

    class Meta:
        verbose_name = "Изображение ресторана"
        verbose_name_plural = "Изображения ресторанов"

    def __str__(self):
        return f"Image {self.id} for {self.restaurant.name}"
