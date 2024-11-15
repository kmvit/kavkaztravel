from django.conf import settings
from django.db import models
from core.models import BaseContent


class Brand(BaseContent):
    """Класс для брэнда машины."""

    name = models.CharField(
        max_length=100, verbose_name="Бренд машины", blank=True, null=True
    )

    def __str__(self):
        return self.name


class Model(BaseContent):
    """Класс для модели машины."""

    name = models.CharField(
        max_length=100, verbose_name="Модель машины", blank=True, null=True
    )

    def __str__(self):
        return self.name


class Year(BaseContent):
    """Класс для года выпуска машины."""

    name = models.CharField(max_length=50, blank=True, null=True)
    year = models.PositiveIntegerField(
        verbose_name="Год выпуска машины", blank=True, null=True
    )


class Color(BaseContent):
    """Класс для года выпуска машины."""

    name = models.CharField(
        max_length=50, verbose_name="Цвет машины", blank=True, null=True
    )

    def __str__(self):
        return self.name


class BodyType(BaseContent):
    """Класс для типа кузова машины."""

    name = models.CharField(
        max_length=100, verbose_name="Тип кузова", blank=True, null=True
    )

    def __str__(self):
        return self.name


class Auto(BaseContent):
    """Класс для модели Машины."""

    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    model = models.ForeignKey(
        Model,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    year = models.ForeignKey(
        Year,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    color = models.ForeignKey(
        Color,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    body_type = models.ForeignKey(
        BodyType,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="auto",
        default=1,
    )

    def __str__(self):
        return str(self.name)


class Foto(models.Model):
    """Класс для модели фото машины."""

    image = models.ImageField(upload_to="content_images/", blank=True, null=True)
    auto = models.ForeignKey(
        Auto, on_delete=models.CASCADE, related_name="Машина", blank=True
    )


class Company(BaseContent):
    """Класс для модели Компа."""

    working_hours = models.TextField(blank=True, null=True)
    auto = models.ManyToManyField(Auto, blank=True, verbose_name="машины")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="company"
    )


class ReviewAuto(models.Model):
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
    auto = models.ForeignKey(
        Auto,
        on_delete=models.CASCADE,
        related_name="auto",
        verbose_name="Машина",
    )
    image = models.ImageField(
        upload_to="content_images/",
        blank=True,
        null=True,
        verbose_name="Изображение отзыва",
        help_text="Опциональное изображение, которое можно прикрепить к отзыву.",
    )
