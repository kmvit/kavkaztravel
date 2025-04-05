from django.conf import settings
from django.db import models
from core.models import BaseContent
from regions.models import Region
from django.core.validators import RegexValidator
from regions.models import Region

 
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


from django.conf import settings
from django.db import models

from django.conf import settings
from django.db import models


class Tour(models.Model):
    """
    Основная модель тура, создаваемого гидом.
    
    Включает информацию о регионе, тематике, достопримечательностях,
    формате проведения, типах участников, стоимости, продолжительности
    и наличии спецпредложения (со скидкой, спецпредложение и пр.).
    """
    guide = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tours",
        verbose_name="Гид тура"
    )
    title = models.CharField(
        max_length=255, unique=True,
        verbose_name="Название тура"
    )
    description = models.TextField("Описание", blank=True, null=True)
    region = models.ForeignKey(
        Region,
        on_delete=models.PROTECT,
        related_name='tours',
        verbose_name="Регион тура"
    )
    attractions = models.ManyToManyField(
        'AttractionTour',
        related_name='tours',
        verbose_name="Достопримечательности тура",
        blank=True
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Стоимость тура"
    )
    theme = models.ForeignKey(
        'ThemeTour',
        on_delete=models.SET_NULL,
        null=True,
        related_name='tours',
        verbose_name="Тематика тура"
    )
    participant_types = models.ManyToManyField(
        'ParticipantTypeTour',
        related_name='tours',
        verbose_name="Типы участников тура",
        blank=True
    )
    formats = models.ManyToManyField(
        'FormatTour',
        related_name='tours',
        verbose_name="Форматы тура",
        blank=True
    )
    duration = models.ForeignKey(
        'DurationTour',
        on_delete=models.PROTECT,
        related_name='tours',
        verbose_name="Продолжительность тура",
        null=True,
        blank=True
    )
    special_offer = models.ForeignKey(
        'SpecialOfferTour',
        on_delete=models.PROTECT,
        related_name='tours',
        verbose_name="Прочее",
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания тура"
    )

    def __str__(self):
        return f"{self.title} ({self.region.name})"

    class Meta:
        verbose_name = "Тур"
        verbose_name_plural = "Туры"


class AttractionTour(models.Model):
    """
    Достопримечательность тура.

    Пример: "Озеро Байкал", "Эльбрус", "Кижи"
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="Название достопримечательности")
    description = models.TextField(blank=True, verbose_name="Описание достопримечательности")
    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        related_name='attractions',
        verbose_name="Регион достопримечательности"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Достопримечательность тура"
        verbose_name_plural = "Достопримечательности туров"



class ThemeTour(models.Model):
    """
    Тематика тура.

    Пример: "Эко-туризм", "Исторический", "Приключения"
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="Название тематики")
    description = models.TextField(blank=True, verbose_name="Описание тематики тура")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тематика тура"
        verbose_name_plural = "Тематики туров"

class ParticipantTypeTour(models.Model):
    """
    Тип участников тура.

    Пример: "Взрослые", "Семьи с детьми", "Пенсионеры"
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="Название типа участников")
    description = models.TextField(blank=True, verbose_name="Описание типа участников")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип участников тура"
        verbose_name_plural = "Типы участников туров"

class FormatTour(models.Model):
    """
    Формат проведения тура.

    Пример: "Групповой", "Индивидуальный", "Онлайн"
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="Название формата")
    description = models.TextField(blank=True, verbose_name="Описание формата участников")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Формат тура"
        verbose_name_plural = "Форматы туров"


class DurationTour(models.Model):
    """
    Модель, описывающая продолжительность тура.
    
    Пример: "2 часа", "3 дня"
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="Продолжительность тура")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Продолжительность тура"
        verbose_name_plural = "Продолжительности туров"

from django.db import models

class SpecialOfferTour(models.Model):
    """
    Модель спецпредложения или скидки для тура.

    В этой модели можно задать тип предложения (например, скидка или спецпредложение),
    """
   
    offer_type = models.CharField(
        max_length=250,
        verbose_name="Тип предложения",
    )
    description = models.TextField(
        verbose_name="Описание",
        blank=True,
        null=True,
        help_text="Описание предложения (например, условия или дополнительные детали)."
    )

    class Meta:
        verbose_name = "Спецпредложение/скидка тура"
        verbose_name_plural = "Спецпредложения/скидки туров"



class GalleryTour(models.Model):
    """Класс для модели галереи фотографий тура.
    Фотографии содержаться в поле  image."""

    tour = models.ForeignKey(
        Tour, on_delete=models.CASCADE, related_name="gallery_tour"
    )
    image = models.ImageField(upload_to="content_images/", blank=True, null=True)



class TourConditions(models.Model):
    """
    Модель, содержащая условия проведения тура:
    - размер группы,
    - наличие детей,
    - место встречи,
    - условия бронирования,
    - организационные детали.
    """

    tour = models.ForeignKey(
        Tour,
        on_delete=models.CASCADE,
        related_name="tour_conditions",
        verbose_name="Тур"
    )
    group_size = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Количество человек в группе"
    )
    children = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Наличие детей в группе"
    )
    meeting_point = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Место встречи"
    )
    booking_terms = models.TextField(
        blank=True,
        null=True,
        verbose_name="Условия бронирования"
    )
    organizational_details = models.TextField(
        blank=True,
        null=True,
        verbose_name="Организационные детали"
    )

    def __str__(self):
        return f"Условия тура для: {self.tour.title}"

    class Meta:
        verbose_name = "Условие тура"
        verbose_name_plural = "Условия туров"


from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class AvailableDateTour(models.Model):
    tour = models.ForeignKey(
        'Tour',
        on_delete=models.CASCADE,
        related_name="available_dates",
        verbose_name="Тур"
    )
    start_date = models.DateField(verbose_name="Дата начала тура")
    end_date = models.DateField(verbose_name="Дата окончания тура")
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активна ли дата"
    )

    class Meta:
        verbose_name = "Доступный период тура"
        verbose_name_plural = "Доступные периоды туров"
        ordering = ["start_date"]

    def __str__(self):
        return f"{self.tour.title}: {self.start_date} — {self.end_date}"

    def clean(self):
        """Проверка корректности дат"""
        # Получаем сегодняшнюю дату
        today = timezone.now().date()

        # Проверяем, что даты не в прошлом
        if self.start_date < today:
            raise ValidationError("Дата начала тура не может быть в прошлом.")
        if self.end_date < today:
            raise ValidationError("Дата окончания тура не может быть в прошлом.")

        # Проверяем, что дата окончания позже даты начала
        if self.end_date <= self.start_date:
            raise ValidationError("Дата окончания тура должна быть позже даты начала.")

    @property
    def duration(self):
        """Вычисляем продолжительность тура как разницу между датой окончания и датой начала."""
        return self.end_date - self.start_date

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
