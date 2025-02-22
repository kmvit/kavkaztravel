from django.conf import settings
from django.db import models


class Car(models.Model):
    """
    Модель автомобиля для каршеринга.
    """
    BODY_TYPES = [
        ('sedan', 'Седан'),
        ('suv', 'Внедорожник'),
        ('hatchback', 'Хэтчбек'),
        ('crossover', 'Кроссовер'),
        ('minivan', 'Минивэн'),
        ('wagon', 'Универсал'),
    ]
    
    BRAND_CHOICES = [
        ('toyota', 'Toyota'),
        ('hyundai', 'Hyundai'),
        ('kia', 'Kia'),
        ('renault', 'Renault'),
        ('nissan', 'Nissan'),
        ('volkswagen', 'Volkswagen'),
        ('lada', 'Lada'),
        ('skoda', 'Skoda'),
        ('mazda', 'Mazda'),
        ('ford', 'Ford'),
    ]
    
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='cars', 
        help_text="Владелец автомобиля",
        verbose_name="Владелец"
    )
    brand = models.CharField(
        max_length=100, 
        choices=BRAND_CHOICES, 
        help_text="Марка автомобиля",
        verbose_name="Марка"
    )
    body_type = models.CharField(
        max_length=20, 
        choices=BODY_TYPES, 
        help_text="Тип кузова автомобиля",
        verbose_name="Тип кузова"
    )
    price_per_day = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        help_text="Стоимость аренды в сутки",
        verbose_name="Цена за день"
    )

    class Meta:
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили"

    def __str__(self):
        return f"{self.get_brand_display()} - {self.get_body_type_display()}"


class CarFeature(models.Model):
    """
    Модель характеристики автомобиля (например, кондиционер, коробка передач и т.д.).
    """
    FEATURE_CHOICES = [
        ('air_conditioning', 'Кондиционер'),
        ('automatic_transmission', 'Автоматическая коробка передач'),
        ('manual_transmission', 'Механическая коробка передач'),
        ('four_doors', '4 двери'),
        ('five_doors', '5 дверей'),
        ('large_trunk', 'Большой багажник'),
    ]
    
    name = models.CharField(
        max_length=100, 
        choices=FEATURE_CHOICES, 
        help_text="Название характеристики",
        verbose_name="Характеристика"
    )
    car = models.ForeignKey(
        Car, 
        on_delete=models.CASCADE, 
        related_name='features', 
        help_text="Автомобиль, которому принадлежит характеристика",
        verbose_name="Автомобиль"
    )

    class Meta:
        verbose_name = "Характеристика автомобиля"
        verbose_name_plural = "Характеристики автомобилей"

    def __str__(self):
        return f"{self.car} - {self.get_name_display()}"


class CarImage(models.Model):
    """
    Модель изображений автомобилей.
    """
    car = models.ForeignKey(
        Car, 
        on_delete=models.CASCADE, 
        related_name='images',
        verbose_name="Автомобиль"
    )
    image = models.ImageField(upload_to='car_images/', verbose_name="Изображение")

    class Meta:
        verbose_name = "Изображение автомобиля"
        verbose_name_plural = "Изображения автомобилей"

    def __str__(self):
        return f"Фото {self.car}"


class RentalCondition(models.Model):
    """
    Модель условий аренды автомобиля.
    """
    car = models.OneToOneField(
        Car, 
        on_delete=models.CASCADE, 
        related_name='rental_condition', 
        help_text="Автомобиль, к которому относятся условия аренды",
        verbose_name="Автомобиль"
    )
    insurance_deposit = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        help_text="Страховой депозит",
        verbose_name="Страховой депозит"
    )
    required_documents = models.TextField(
        help_text="Необходимые документы для аренды",
        verbose_name="Необходимые документы"
    )
    min_driver_age = models.IntegerField(
        help_text="Минимальный возраст водителя",
        verbose_name="Минимальный возраст водителя"
    )
    min_driving_experience = models.IntegerField(
        help_text="Минимальный стаж вождения (в годах)",
        verbose_name="Минимальный стаж вождения"
    )
    rental_start_date = models.DateTimeField(
        help_text="Дата начала аренды",
        verbose_name="Дата начала аренды"
    )
    rental_end_date = models.DateTimeField(
        help_text="Дата окончания аренды",
        verbose_name="Дата окончания аренды"
    )

    class Meta:
        verbose_name = "Условия аренды"
        verbose_name_plural = "Условия аренды"

    def __str__(self):
        return f"Условия аренды для {self.car}"
