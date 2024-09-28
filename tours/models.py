from django.conf import settings
from django.db import models
from core.models import BaseContent
from regions.models import Region


class Guide(BaseContent):
    """Класс для модели гид."""
    region = models.ForeignKey(Region, on_delete=models.CASCADE,
                               related_name='guides')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE, related_name='guides')
    experience = models.IntegerField()  # Years of experience

    def __str__(self):
        return self.name


class TourOperator(BaseContent):
    """Класс для модели фирмы туроператор."""
    region = models.ForeignKey(Region, on_delete=models.CASCADE,
                               related_name='touroperators')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,
                              related_name='touroperators')
    license_number = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tour(BaseContent):
    """Класс для модели тура."""
    tour_operator = models.ForeignKey(TourOperator, on_delete=models.CASCADE,
                               related_name='touroperators')


class GalleryTour(BaseContent):
    """Класс для модели галереи фотографий тура.
    Фотографии содержаться в поле  image."""
    tour = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,
                              related_name='tour')


class EstimationTour(BaseContent):
    """Класс для модели, который содержит оценки и отзывы."""
    tour = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,
                              related_name='tour')
    estimation = models.IntegerField(blank=True, 
                                     null=True, 
                                     verbose_name="Оценка тура",
                                     choices=list(zip(range(1, 10), range(1, 10))))
    feedback = models.TextField(blank=True, null=True, verbose_name="Отзыв")


class DateTour(BaseContent):
    """Класс для модели, которая содержит 
    даты начало и конца тура."""
    tour = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,
                              related_name='tour')
    name = models.CharField(max_length=100, blank=True, null=True)
    begin_date = models.DateField(verbose_name="Начало тура",)
    end_date = models.DateField(verbose_name="Конец тура",)
    is_free = models.BooleanField(default = True)


class TourConditions(BaseContent):
    """Класс для модели, которая содержит условия тура.
    Продолжительность, количество человек в группе,
    наличие детей в группе, стоимость. 
    """
    tour = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,
                              related_name='tour')
    name = models.CharField(max_length=100, blank=True, null=True)
    duration =  models.IntegerField(blank=True, null=True)
    group_size = models.IntegerField(blank=True, null=True)
    children = models.CharField(max_length=100, blank=True, null=True)
    transport = models.CharField(max_length=100, blank=True, null=True)
    cost = models.IntegerField(blank=True, null=True)


class Order(BaseContent):
    """Класс для модели заказа тура. Содержит информацию
    о заказчике тура и предполагаемой дате тура."""
    tour = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,
                              related_name='tour')
    name = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField()
    size =  models.IntegerField(blank=True, null=True)
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