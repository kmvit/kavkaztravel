from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from core.models import BaseContent, BaseReview, BaseReviewImage
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


class ReviewEntertainment(BaseReview):
    """Класс для модели, который содержит оценки и отзывы о развлечениях или местах отдыха.

    Эта модель используется для хранения отзывов и рейтингов, оставленных пользователями о гостиницах
    или развлекательных местах. Каждый отзыв включает оценку, комментарий, изображение и дату создания.
    """

    
    entertainment = models.ForeignKey(
        "Entertainment",  # Здесь предполагается наличие модели Entertainment
        on_delete=models.CASCADE,
        related_name="entertainment",  # Лучше использовать более универсальное имя для связки
        verbose_name="Развлекательное место",
    )
    
    def __str__(self):
        return f"Отзыв от {self.owner} о {self.entertainment}"


class ReviewImageEntertainment(BaseReviewImage):
    """Модель для хранения изображения отзыва, связанного с конкретным отзывом."""

    review = models.ForeignKey(
        ReviewEntertainment,  # Связь с моделью ReviewHotel (отзыв)
        on_delete=models.CASCADE,
        related_name="review_images",  # Все изображения этого отзыва
        verbose_name="Отзыв",
        help_text="Отзыв, к которому привязано изображение.",
    )
