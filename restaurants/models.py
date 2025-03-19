from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from Kavkaztome import settings
from core.models import BaseContent
from regions.models import Region


class Restaurant(BaseContent):
    address = models.CharField(max_length=300)
    region = models.ForeignKey(
        Region, on_delete=models.CASCADE, related_name="restaurants"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="restaurants",
        default=1,
    )

    class Meta:
        verbose_name = "Объект питания"
        verbose_name_plural = "Объекты питания"

    def __str__(self):
        return self.name

   
class RestaurantImage(models.Model):
    restaurant = models.ForeignKey(
        Restaurant, related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField()

    def __str__(self):
        return self.restaurant.id
