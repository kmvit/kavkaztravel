from django.conf import settings
from django.db import models


from django.db import models
from django.conf import settings


class RentalDiscount(models.Model):
    """
    Модель для хранения скидок на аренду в зависимости от срока.
    """

    name = models.CharField(
        max_length=50,
        help_text="Название скидки (например, 'Стандартные скидки')",
        verbose_name="Название",
    )
    discount_week = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        help_text="Скидка в % при аренде от 7 дней",
        verbose_name="Скидка на неделю",
    )
    discount_month = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        help_text="Скидка в % при аренде от 30 дней",
        verbose_name="Скидка на месяц",
    )

    def get_discount(self, days: int) -> float:
        """
        Возвращает соответствующую скидку в зависимости от количества дней аренды.
        """
        if days >= 30:
            return self.discount_month / 100  # Преобразуем в коэффициент
        elif days >= 7:
            return self.discount_week / 100
        return 0  # Без скидки

    def __str__(self):
        return self.name


class Car(models.Model):
    """
    Модель автомобиля для каршеринга.
    """

    BODY_TYPES = [
        ("sedan", "Седан"),
        ("suv", "Внедорожник"),
        ("hatchback", "Хэтчбек"),
        ("crossover", "Кроссовер"),
        ("minivan", "Минивэн"),
        ("wagon", "Универсал"),
    ]

    BRAND_CHOICES = [
        ("toyota", "Toyota"),
        ("hyundai", "Hyundai"),
        ("kia", "Kia"),
        ("renault", "Renault"),
        ("nissan", "Nissan"),
        ("volkswagen", "Volkswagen"),
        ("lada", "Lada"),
        ("skoda", "Skoda"),
        ("mazda", "Mazda"),
        ("ford", "Ford"),
    ]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cars",
        verbose_name="Владелец",
    )
    brand = models.CharField(
        max_length=100, choices=BRAND_CHOICES, verbose_name="Марка"
    )
    body_type = models.CharField(
        max_length=20, choices=BODY_TYPES, verbose_name="Тип кузова"
    )
    price_per_day = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Цена за день"
    )
    discount_policy = models.ForeignKey(
        RentalDiscount,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="rental_cars",
        verbose_name="Политика скидок",
    )

    def calculate_rental_price(self, days: int) -> float:
        """
        Рассчитывает стоимость аренды в зависимости от количества дней и скидок.
        """
        discount = (
            self.discount_policy.get_discount(days) if self.discount_policy else 0
        )
        print(discount, 1)
        daily_price = self.price_per_day * (1 - discount)
        print(daily_price, 2)
        return round(daily_price * days, 2)

    class Meta:
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили"


class CarFeature(models.Model):
    """
    Модель характеристики автомобиля (например, кондиционер, коробка передач и т.д.).
    """

    FEATURE_CHOICES = [
        ("air_conditioning", "Кондиционер"),
        ("automatic_transmission", "Автоматическая коробка передач"),
        ("manual_transmission", "Механическая коробка передач"),
        ("four_doors", "4 двери"),
        ("five_doors", "5 дверей"),
        ("large_trunk", "Большой багажник"),
    ]

    name = models.CharField(
        max_length=100,
        choices=FEATURE_CHOICES,
        help_text="Название характеристики",
        verbose_name="Характеристика",
    )
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name="features",
        help_text="Автомобиль, которому принадлежит характеристика",
        verbose_name="Автомобиль",
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
        Car, on_delete=models.CASCADE, related_name="images", verbose_name="Автомобиль"
    )
    image = models.ImageField(upload_to="car_images/", verbose_name="Изображение")

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
        related_name="rental_condition",
        help_text="Автомобиль, к которому относятся условия аренды",
        verbose_name="Автомобиль",
    )
    insurance_deposit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Страховой депозит",
        verbose_name="Страховой депозит",
    )
    required_documents = models.TextField(
        help_text="Необходимые документы для аренды",
        verbose_name="Необходимые документы",
    )
    min_driver_age = models.IntegerField(
        help_text="Минимальный возраст водителя",
        verbose_name="Минимальный возраст водителя",
    )
    min_driving_experience = models.IntegerField(
        help_text="Минимальный стаж вождения (в годах)",
        verbose_name="Минимальный стаж вождения",
    )

    class Meta:
        verbose_name = "Условия аренды"
        verbose_name_plural = "Условия аренды"

    def __str__(self):
        return f"Условия аренды для {self.car}"


class Rental(models.Model):
    """Модель аренды автомобиля с расчетом общей стоимости на основе дат аренды"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Арендатор"
    )
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name="Автомобиль")
    pickup_datetime = models.DateTimeField(verbose_name="Дата и время получения")
    return_datetime = models.DateTimeField(verbose_name="Дата и время возврата")
    daily_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Цена за день"
    )
    return_location = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Место возврата"
    )

    class Meta:
        verbose_name = "Аренда"
        verbose_name_plural = "Аренды"

    def calculate_total_price_with_discount(self):
        """Метод для расчета общей стоимости аренды с учетом скидок."""
        if not self.pickup_datetime or not self.return_datetime:
            return None  # Если даты не заданы, возвращаем None

        duration = self.return_datetime - self.pickup_datetime
        print(duration)
        days = max(duration.days, 1)  # Минимально 1 день
        print(days)
        return self.car.calculate_rental_price(days)
