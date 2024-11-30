from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Review(models.Model):
    """
    Модель для отзывов, которая связывает пользователя с конкретным объектом.

    Ограничения:
    - Уникальное сочетание (owner, content_type, object_id): Один пользователь может оставить только один отзыв на конкретный объект.
    """

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата отзыва")
    text = models.TextField(verbose_name="Текст отзыва", blank=True, null=True)
    rating = models.IntegerField(verbose_name="Оценка", null=True, blank=True)  # Для тех сущностей, где есть рейтинг
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, verbose_name="Тип сущности"
    )
    object_id = models.PositiveIntegerField(verbose_name="ID сущности")
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        unique_together = ("owner", "content_type", "object_id")
        

class ReviewPhoto(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="photos")
    image = models.ImageField(upload_to="review_photos/", verbose_name="Фотография")
    caption = models.CharField(max_length=255, verbose_name="Описание", blank=True)

    class Meta:
        verbose_name = "Фотография отзыва"
        verbose_name_plural = "Фотографии отзывов"

