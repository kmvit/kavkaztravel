from django.conf import settings
from django.db import models
from core.models import BaseContent, BaseReview, BaseReviewImage
from regions.models import Region
from django.core.validators import RegexValidator


class Guide(BaseContent):
    """
    Класс для модели гид.
    """

    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="guides")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="guides",
        default=1,
    )
    experience = models.IntegerField()


class TourOperator(BaseContent):
    """Класс для модели фирмы туроператор."""

    region = models.ForeignKey(
        Region, on_delete=models.CASCADE, related_name="touroperators"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="touroperators",
        default=1,
    )
    license_number = models.CharField(max_length=100)

    def __str__(self):
        return self.license_number


class Tour(models.Model):
    """Класс для модели тура."""

    tour_operator = models.ForeignKey(
        TourOperator, on_delete=models.CASCADE, related_name="touroperators"
    )
    tag = models.ForeignKey("Tag", on_delete=models.CASCADE, related_name="tag")
    geo = models.ForeignKey("Geo", on_delete=models.CASCADE, related_name="tag")
    name = models.CharField(max_length=100)
    content = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True, null=True)
    slug = models.SlugField(unique=True, blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tour",
        default=1,
    )

    def __str__(self):
        return self.name

    def calculate_rating(self):
        reviews = self.reviews.all()
        total_rating = sum(review.rating for review in reviews)
        return total_rating / reviews.count() if reviews.exists() else 0


class Geo(models.Model):
    geo_title = models.CharField(max_length=255, blank=True, null=True)
    geo_description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.geo_title


class GalleryTour(models.Model):
    """Класс для модели галереи фотографий тура.
    Фотографии содержаться в поле  image."""

    tour = models.ForeignKey(
        Tour, on_delete=models.CASCADE, related_name="gallery_tour"
    )
    image = models.ImageField(upload_to="content_images/", blank=True, null=True)


class ReviewTour(BaseReview):
    """Класс для модели, который содержит оценки и отзывы о туре.

    Эта модель используется для хранения отзывов и рейтингов, оставленных пользователями на
    определенный тур. Каждый отзыв включает оценку, комментарий и дату создания.
    """

    tour = models.ForeignKey(
        Tour,
        on_delete=models.CASCADE,
        related_name="tour",
        verbose_name="tour",
        help_text="Тур, к которому относится этот отзыв.",
    )


class ReviewImageTour(BaseReviewImage):
    """Модель для хранения изображения отзыва, связанного с конкретным отзывом."""

    review = models.ForeignKey(
        ReviewTour,
        on_delete=models.CASCADE,
        related_name="review_images",
        verbose_name="Фотографии отзывов тура",
        help_text="Тур, к которому привязано изображение отзыва.",
    )


class DateTour(models.Model):
    """Класс для модели, которая содержит
    даты начало и конца тура."""

    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="date_tour")
    begin_date = models.DateField(
        verbose_name="Начало тура",
    )
    end_date = models.DateField(
        verbose_name="Конец тура",
    )
    is_free = models.BooleanField(default=True)


class TourConditions(models.Model):
    """Класс для модели, которая содержит условия тура.
    Продолжительность, количество человек в группе,
    наличие детей в группе, стоимость.
    """

    tour = models.ForeignKey(
        Tour, on_delete=models.CASCADE, related_name="tour_conditions"
    )
    duration = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Продолжительность тура",
    )
    group_size = models.IntegerField(
        blank=True, null=True, verbose_name="Количество человек"
    )
    children = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Наличие детей"
    )
    transport = models.CharField(max_length=100, blank=True, null=True)
    cost = models.PositiveIntegerField(
        blank=True, null=True, verbose_name="Стоимость тура"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="conditions",
        default=1,
    )


class Order(models.Model):
    """Класс для модели заказа тура. Содержит информацию
    о заказчике тура и предполагаемой дате тура."""

    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="order")
    date = models.DateField()
    size = models.IntegerField(blank=True, null=True)
    username = models.CharField(max_length=150)
    email = models.EmailField(blank=True)
    phone = models.CharField(
        max_length=50,
        verbose_name="Номер телефона",
        validators=[
            RegexValidator(
                regex=r"^\+7\d{10}$",
                message="Номер должен быть в формате +7XXXXXXXXXX",
            )
        ],
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owner",
        default=1,
    )


class Tag(models.Model):
    """Класс для работы таблицы тэг."""

    name = models.CharField(
        max_length=200,
        verbose_name="Название",
    )

    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name
