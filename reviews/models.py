from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from kashiring.models import Auto
from django.db import models


class Review(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="reviews", 
        verbose_name="Пользователь"
)
    car = models.ForeignKey(Auto, on_delete=models.CASCADE, related_name="reviews", verbose_name="Автомобиль")
    text = models.TextField(verbose_name="Текст отзыва", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_approved = models.BooleanField(default=False, verbose_name="Одобрено")

    def __str__(self):
        return f"Отзыв от {self.user} о {self.car}"

class ReviewImage(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="images", verbose_name="Отзыв")
    image = models.ImageField(upload_to="review_images/", verbose_name="Изображение")

    def __str__(self):
        return f"Фото для {self.review}"


class Rating(models.Model):
    CRITERIA_CHOICES = [
        ("cleanliness", "Чистота салона"),
        ("service", "Качество обслуживания"),
        ("location", "Расположение"),
        ("photo_match", "Соответствие фото"),
        ("price_quality", "Цена/качество"),
    ]

    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="ratings", verbose_name="Отзыв")
    criteria = models.CharField(max_length=20, choices=CRITERIA_CHOICES, verbose_name="Критерий")
    score = models.PositiveIntegerField(
        verbose_name="Оценка (1-10)", 
        validators=[MinValueValidator(1), MaxValueValidator(10)]  # ✅ Ограничение от 1 до 10
    )

    def __str__(self):
        return f"{self.criteria}: {self.score} для {self.review}"
