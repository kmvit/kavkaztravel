from django.conf import settings
from django.db import models
from core.models import BaseContent



lass Car(models.Model):
    """
    Модель автомобиля для каршеринга.
    
    Атрибуты:
        owner (User): Владелец автомобиля.
        brand (str): Марка автомобиля.
        body_type (str): Тип кузова автомобиля (выбирается из списка).
        price_per_day (Decimal): Стоимость аренды в сутки.
    """
    BODY_TYPES = [
        ('sedan', 'Sedan'),
        ('suv', 'SUV'),
        ('hatchback', 'Hatchback'),
        ('crossover', 'Crossover'),
        ('minivan', 'Minivan'),
        ('wagon', 'Wagon'),
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
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cars', help_text="Владелец автомобиля")
    brand = models.CharField(max_length=100, choices=BRAND_CHOICES, help_text="Марка автомобиля")
    body_type = models.CharField(max_length=20, choices=BODY_TYPES, help_text="Тип кузова автомобиля")
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2, help_text="Стоимость аренды в сутки")
    
    def __str__(self):
        """Возвращает строковое представление автомобиля."""
        return f"{self.brand}'s {self.body_type}



class CarFeature(models.Model):
    """
    Модель характеристики автомобиля (например, кондиционер, коробка передач и т.д.).
    
    Атрибуты:
        name (str): Название характеристики.
        value (str): Значение характеристики (например, "Автоматическая" для коробки передач).
        car (ForeignKey): Связь с конкретным автомобилем.
    """
  
    FEATURE_CHOICES = [
        ('air_conditioning', 'Кондиционер'),
        ('automatic_transmission', 'Автоматическая коробка передач'),
        ('manual_transmission', 'Механическая коробка передач'),
        ('four_doors', '4 двери'),
        ('five_doors', '5 дверей'),
        ('large_trunk', 'Большой багажник'),
    ]
    
    name = models.CharField(max_length=100, choices=FEATURE_CHOICES, help_text="Название характеристики")
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='features', help_text="Автомобиль, которому принадлежит характеристика")
    
    def __str__(self):
        """Возвращает строковое представление характеристики."""
        return f"{self.car.owner.username}'s {self.car.body_type} - {self.name}: {self.value}"

class RentalCondition(models.Model):
    """
    Модель условий аренды автомобиля.
    """
    car = models.OneToOneField(Car, on_delete=models.CASCADE, related_name='rental_condition', help_text="Автомобиль, к которому относятся условия аренды")
    insurance_deposit = models.DecimalField(max_digits=10, decimal_places=2, help_text="Страховой депозит")
    required_documents = models.TextField(help_text="Необходимые документы для аренды")
    min_driver_age = models.IntegerField(help_text="Минимальный возраст водителя")
    min_driving_experience = models.IntegerField(help_text="Минимальный стаж вождения (в годах)")
    rental_start_date = models.DateTimeField(help_text="Дата начала аренды")
    rental_end_date = models.DateTimeField(help_text="Дата окончания аренды")
    
    def __str__(self):
        """Возвращает строковое представление условий аренды."""
        return f"Условия аренды для {self.car.owner.username}'s {self.car.body_type}"