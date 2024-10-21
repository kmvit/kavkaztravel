from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from core.models import BaseContent
from Kavkaztome import settings
from reviews.models import Review


class Region(BaseContent):
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    reviews = GenericRelation(Review, related_query_name="reviews")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1
    )

    class Meta:
        verbose_name = "Регион/город"
        verbose_name_plural = "Регионы/города"

    def __str__(self):
        return self.name


class RegionImage(models.Model):
    region = models.ForeignKey(Region, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField()

    def __str__(self):
        return self.region.id
