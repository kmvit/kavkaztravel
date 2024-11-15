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


class ReviewRestaurant(models.Model):
    """Класс для модели, который содержит оценки и отзывы о местах общественного питания.

    Эта модель используется для хранения отзывов и рейтингов, оставленных пользователями на
    определенный местах общественного питания. Каждый отзыв включает оценку, комментарий, изображение и дату создания.
    """

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        default=1,
        verbose_name="Владелец отзыва",
        help_text="Пользователь, оставивший отзыв.",
    )
    rating = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name="Оценка тура",
        choices=list(zip(range(1, 6), range(1, 6))),
        help_text="Оценка тура от 1 до 5, где 1 - плохо, а 5 - отлично.",
    )
    comment = models.TextField(
        verbose_name="Комментарий",
        help_text="Текстовый комментарий к туру. Пользователь может оставить свой отзыв.",
    )
    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата отзыва",
        help_text="Дата и время создания отзыва.",
    )
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name="restaurant",
        verbose_name="Место общественного питания",
    )
    image = models.ImageField(
        upload_to="content_images/",
        blank=True,
        null=True,
        verbose_name="Изображение отзыва",
        help_text="Опциональное изображение, которое можно прикрепить к отзыву.",
    )
