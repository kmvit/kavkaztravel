from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from Kavkaztome import settings
from core.models import BaseContent, BaseReview, BaseReviewImage
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


class ReviewRestaurant(BaseReview):
    """Класс для модели, который содержит оценки и отзывы о местах общественного питания.

    Эта модель используется для хранения отзывов и рейтингов, оставленных пользователями на
    определенный местах общественного питания. Каждый отзыв включает оценку, комментарий, изображение и дату создания.
    """

    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name="restaurant",
        verbose_name="Место общественного питания",
    )
    
class ReviewImageRestaurant(BaseReviewImage):
    """Модель для хранения изображения отзыва, связанного с конкретным отзывом."""

    review = models.ForeignKey(
        ReviewRestaurant,
        on_delete=models.CASCADE,
        related_name="review_images",
        verbose_name="Место общественного питания",
        help_text="Место общественного питания, к которому привязано изображение отзыва.",
    )
