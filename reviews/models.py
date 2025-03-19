from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from kashiring.models import Car
from django.db import models


class CarReview(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="car_reviews",
        verbose_name="Пользователь",
    )
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name="car_reviews",
        verbose_name="Автомобиль",
    )
    text = models.TextField(verbose_name="Текст отзыва", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_approved = models.BooleanField(default=False, verbose_name="Одобрено")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return f"Отзыв от {self.user} о {self.car}"


class CarReviewImage(models.Model):
    car_review = models.ForeignKey(
        CarReview, on_delete=models.CASCADE, related_name="car_images", verbose_name="Отзыв"
    )
    image = models.ImageField(upload_to="car_review_images/", verbose_name="Изображение")

    class Meta:
        verbose_name = "Изображение отзыва"
        verbose_name_plural = "Изображения отзывов"

    def __str__(self):
        return f"Фото для {self.car_review}"


class CarRating(models.Model):
    CRITERIA_CHOICES = [
        ("cleanliness", "Чистота салона"),
        ("service", "Качество обслуживания"),
        ("location", "Расположение"),
        ("photo_match", "Соответствие фото"),
        ("price_quality", "Цена/качество"),
    ]

    car_review = models.ForeignKey(
        CarReview, on_delete=models.CASCADE, related_name="ratings", verbose_name="Отзыв"
    )
    criteria = models.CharField(
        max_length=20, choices=CRITERIA_CHOICES, verbose_name="Критерий"
    )
    score = models.PositiveIntegerField(
        verbose_name="Оценка (1-10)",
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )

    class Meta:
        verbose_name = "Оценка"
        verbose_name_plural = "Оценки"

    def __str__(self):
        return f"{self.criteria}: {self.score} для {self.car_review}"
