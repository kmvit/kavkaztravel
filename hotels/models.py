from datetime import date
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from Kavkaztome import settings
from core.models import BaseContent, BaseReview, BaseReviewImage
from regions.models import Region


class Tag(models.Model):
    """
    Модель для представления тегов.

    Теги могут использоваться для классификации и фильтрации различных
    объектов, таких как гостиницы или удобства. Каждый тег имеет имя
    и иконку.

    """

    name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to="tag_icons/")

    def __str__(self):
        return self.name


class MealPlan(models.Model):
    """
    Модель для представления планов питания.

    Планы питания описывают различные варианты меню, доступные для
    гостей, включая название и описание.

    """

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class AccommodationType(models.Model):
    """
    Модель для представления типов размещения.

    Типы размещения описывают различные варианты проживания, включая
    название и описание.

    """

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Amenity(models.Model):
    """
    Модель для представления удобств.

    Удобства описывают дополнительные услуги, предлагаемые в гостинице,
    включая название и описание.

    """

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Hotel(BaseContent):
    """
    Модель для представления гостиниц.

    Эта модель описывает гостиницы, включая адрес, регион, владельца,
    теги и рецензии. Она также позволяет вычислять средний рейтинг
    на основе связанных рецензий.

    """

    address = models.CharField(max_length=300)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="hotels")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="hotels",
        default=1,
    )
    tags = models.ManyToManyField(Tag, related_name="hotels")

    class Meta:
        verbose_name = "Гостиница"
        verbose_name_plural = "Гостиницы"

    def __str__(self):
        return self.name


class HotelImage(models.Model):
    """
    Модель для хранения изображений гостиниц.

    Эта модель связывает изображения с конкретными гостиницами,
    позволяя хранить множественные изображения для каждой гостиницы.
    """

    hotel = models.ForeignKey(Hotel, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField()

    def __str__(self):
        return self.hotel.id


class Room(models.Model):
    """
    Модель для представления номеров гостиниц.

    Эта модель описывает номера в гостиницах, включая название,
    описание, цену и вместимость.
    """

    hotel = models.ForeignKey(Hotel, related_name="rooms", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.IntegerField()
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="room"
    )

    def __str__(self):
        return f"{self.hotel.name} - {self.name}"


class RoomImage(models.Model):
    """
    Модель для хранения изображений номеров гостиниц.

    Эта модель связывает изображения с конкретными номерами,
    позволяя хранить множественные изображения для каждого номера.
    """

    room = models.ForeignKey(Room, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="room_images/")

    def __str__(self):
        return f"Image for {self.room.name}"


class RoomPrice(models.Model):
    """
    Модель для представления цен на номера в зависимости от сезона.

    Эта модель хранит информацию о ценах на номера в разные
    сезоны и для различных дат.
    Метаданные:
        unique_together (tuple): Уникальное сочетание номера и даты
            для предотвращения дублирования записей.
    Методы:
        __str__(): Возвращает строку с информацией о цене на номер
            на указанную дату.
    Свойства:
        is_high_season (bool): Возвращает True, если сезон высокий
            или праздничный и месяц - декабрь или январь.
        is_low_season (bool): Возвращает True, если сезон низкий
            или праздничный и месяц не декабрь или январь.
    """

    SEASONS = (
        ("low", "Low Season"),
        ("high", "High Season"),
        ("holiday", "Holiday Season"),
    )
    room = models.ForeignKey(Room, related_name="prices", on_delete=models.CASCADE)
    date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    season = models.CharField(max_length=10, choices=SEASONS, default="low")

    class Meta:
        unique_together = ("room", "date")

    def __str__(self):
        return f"{self.room.name} - {self.date}: {self.price}"

    @property
    def is_high_season(self):
        today = date.today()
        return self.season == "high" or (
            self.season == "holiday" and today.month in [12, 1]
        )

    @property
    def is_low_season(self):
        today = date.today()
        return self.season == "low" or (
            self.season == "holiday" and today.month not in [12, 1]
        )


class ReviewHotel(BaseReview):
    """Класс для модели, который содержит оценки и отзывы о гости.

    Эта модель используется для хранения отзывов и рейтингов, оставленных пользователями о гостиницах
    определенный местах общественного питания. Каждый отзыв включает оценку, комментарий, изображение и дату создания.
    """

    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name="hotel",
        verbose_name="Гостиница",
    )
  

class ReviewImageHotel(BaseReviewImage):
    """Модель для хранения изображения отзыва, связанного с конкретным отзывом."""
    
    review = models.ForeignKey(
        ReviewHotel,  # Связь с моделью ReviewHotel (отзыв)
        on_delete=models.CASCADE,
        related_name="review_images",  # Все изображения этого отзыва
        verbose_name="Отзыв",
        help_text="Отзыв, к которому привязано изображение.",
    )
