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


class GalleryTour(models.Model):
    """Класс для модели галереи фотографий тура.
    Фотографии содержаться в поле  image."""
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE,
                              related_name='tour')
    image = models.ImageField(upload_to='content_images/', blank=True,
                              null=True)
    


class EstimationTour(models.Model):
    """Класс для модели, который содержит оценки и отзывы."""
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE,
                              related_name='tour')
    estimation = models.IntegerField(blank=True, 
                                     null=True, 
                                     verbose_name="Оценка тура",
                                     choices=list(zip(range(1, 10), range(1, 10))))
    feedback = models.TextField(blank=True, null=True, verbose_name="Отзыв")
    image = models.ImageField(upload_to='content_images/', blank=True,
                              null=True)
    date = models.DateField(auto_now_add=True, null=True)


class DateTour(models.Model):
    """Класс для модели, которая содержит 
    даты начало и конца тура."""
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE,
                              related_name='tour')
    begin_date = models.DateField(verbose_name="Начало тура",)
    end_date = models.DateField(verbose_name="Конец тура",)
    is_free = models.BooleanField(default = True)


class TourConditions(models.Model):
    """Класс для модели, которая содержит условия тура.
    Продолжительность, количество человек в группе,
    наличие детей в группе, стоимость. 
    """
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE,
                              related_name='tour')
    duration = models.IntegerField(blank=True, null=True, 
                                   verbose_name="Продолжительность тура",)
    group_size = models.IntegerField(blank=True, null=True,
                                     verbose_name="Количество человек")
    children = models.CharField(max_length=100, blank=True, null=True,
                                verbose_name="Наличие детей")
    transport = models.CharField(max_length=100, blank=True, null=True)
    cost = models.IntegerField(blank=True, null=True, 
                               verbose_name="Стоимость тура")


class Order(models.Model):
    """Класс для модели заказа тура. Содержит информацию
    о заказчике тура и предполагаемой дате тура."""
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE,
                              related_name='tour')
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