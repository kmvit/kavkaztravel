from django.conf import settings
from django.db import models
from django.utils import timezone


class BaseContent(models.Model):
    """Базовый класс для моделей."""

    name = models.CharField(max_length=100)
    url = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True, null=True)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="content_images/", blank=True, null=True)
    seo_title = models.CharField(max_length=255, blank=True, null=True)
    seo_description = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True

    
class BaseReview(models.Model):
    """Класс для базовой модели, который содержит оценки и отзывы.

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


class BaseReviewImage(models.Model):
    """
    Класс для базовой модели, который содержит изображения, 
    которые могут быть загружены при формировании отзыва.

    """
    
    image = models.ImageField(
        upload_to="review_images/",
        verbose_name="Изображение отзыва",
        help_text="Изображение, связанное с отзывом.",
    )