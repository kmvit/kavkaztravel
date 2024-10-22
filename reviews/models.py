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
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1
    )
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("owner", "content_type", "object_id")
