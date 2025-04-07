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


class Tour(models.Model):
    """
    Основная модель тура, создаваемого гидом.
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
    terms = models.TextField(
        "Условия тура",
        blank=True,
        null=True,
        help_text="Правила отмены, что включено в стоимость, требования к участникам и т.д."
    )
    region = models.ForeignKey(
        Region,
        on_delete=models.PROTECT,
        related_name='tours',
        verbose_name="Регион тура"
    )
    tags = models.ManyToManyField(
        'Tag',
        related_name='tours',
        verbose_name="Теги тура",
        blank=True
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Стоимость тура"
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

class Tag(models.Model):
    """
    Универсальная модель для тегов.
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="Название тега")
    description = models.TextField(blank=True, null=True, verbose_name="Описание тега")
    tag_type = models.CharField(max_length=50, verbose_name="Тип тега")  # теперь любой тип

    def __str__(self):
        return f"{self.name} ({self.tag_type})"

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"



class GalleryTour(models.Model):
    """Класс для модели галереи фотографий тура.
    Фотографии содержаться в поле  image."""

    tour = models.ForeignKey(
        Tour, on_delete=models.CASCADE, related_name="gallery_tour"
    )
    image = models.ImageField(upload_to="content_images/", blank=True, null=True)



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
