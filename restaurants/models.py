from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from Kavkaztome import settings
from core.models import BaseContent
from regions.models import Region
from reviews.models import Review


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
    reviews = GenericRelation(Review, related_query_name="reviews")

    class Meta:
        verbose_name = "Объект питания"
        verbose_name_plural = "Объекты питания"

    def __str__(self):
        return self.name

    def calculate_rating(self):
        reviews = self.reviews.all()
        total_rating = sum(review.rating for review in reviews)
        return total_rating / reviews.count() if reviews.exists() else 0


class RestaurantImage(models.Model):
    restaurant = models.ForeignKey(
        Restaurant, related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField()

    def __str__(self):
        return self.restaurant.id
