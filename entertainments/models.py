from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from core.models import BaseContent
from Kavkaztome import settings
from regions.models import Region


class Entertainment(BaseContent):
    """Модель для представления развлекательных объектов.

    Эта модель описывает развлекательные объекты, включая адрес,
    регион и владельца. Также поддерживается связь с рецензиями и
    возможностью получения изображений, связанных с объектом.
    Методы:
        __str__(): Возвращает имя объекта.
        calculate_rating(): Вычисляет средний рейтинг на основе
            связанных рецензий.
    """

    address = models.CharField(max_length=300)
    region = models.ForeignKey(
        Region, on_delete=models.CASCADE, related_name="entertainments"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1
    )

    class Meta:
        verbose_name = "Достопримечательность"
        verbose_name_plural = "Достопримечательности"

    def __str__(self):
        return self.name

    def calculate_rating(self):
        reviews = self.reviews.all()
        total_rating = sum(review.rating for review in reviews)
        return total_rating / reviews.count() if reviews.exists() else 0


class EntertainmentImage(models.Model):
    """Модель для хранения изображений развлекательных объектов.

    Эта модель связывает изображения с конкретными развлекательными
    объектами, позволяя хранить множественные изображения для каждого
    объекта.

    """

    entertainment = models.ForeignKey(
        Entertainment, related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField()

    def __str__(self):
        return self.entertainment.id


class ReviewEntertainment(models.Model):
    """Класс для модели, который содержит оценки и отзывы о развлечениях или местах отдыха.

    Эта модель используется для хранения отзывов и рейтингов, оставленных пользователями о гостиницах
    или развлекательных местах. Каждый отзыв включает оценку, комментарий, изображение и дату создания.
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
        verbose_name="Оценка",
        choices=[(i, i) for i in range(1, 6)],
        help_text="Оценка от 1 до 5, где 1 - плохо, а 5 - отлично.",
    )
    comment = models.TextField(
        verbose_name="Комментарий",
        help_text="Текстовый комментарий к месту развлечения или гостинице. Пользователь может оставить свой отзыв.",
    )
    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата отзыва",
        help_text="Дата и время создания отзыва.",
    )
    entertainment = models.ForeignKey(
        "Entertainment",  # Здесь предполагается наличие модели Entertainment
        on_delete=models.CASCADE,
        related_name="entertainment",  # Лучше использовать более универсальное имя для связки
        verbose_name="Развлекательное место",
    )
    image = models.ImageField(
        upload_to="content_images/",
        blank=True,
        null=True,
        verbose_name="Изображение отзыва",
        help_text="Опциональное изображение, которое можно прикрепить к отзыву.",
    )

    class Meta:
        unique_together = [
            "owner",
            "entertainment",
        ]  # Отзыв должен быть уникален для каждого владельца и развлекательного места
        verbose_name = "Отзыв о развлечении"
        verbose_name_plural = "Отзывы о развлечениях"

    def __str__(self):
        return f"Отзыв от {self.owner} о {self.entertainment}"
