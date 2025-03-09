from django.conf import settings
from django.db import models



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

    DRIVE_TYPES = [
        ("fwd", "Передний привод"),
        ("rwd", "Задний привод"),
        ("awd", "Полный привод"),
    ]

    ENGINE_TYPES = [
        ("petrol", "Бензиновый"),
        ("diesel", "Дизельный"),
        ("electric", "Электрический"),
        ("hybrid", "Гибридный"),
    ]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cars",
        verbose_name="Владелец",
    )
    model = models.ForeignKey(
        "Model",
        on_delete=models.CASCADE,
        related_name="cars",
        verbose_name="Марка",
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание автомобиля",
        help_text="Описание автомобиля (необязательное поле)"
    )
    body_type = models.CharField(
        max_length=20, choices=BODY_TYPES, verbose_name="Тип кузова"
    )
    year_of_production = models.PositiveIntegerField(
        verbose_name="Год выпуска",
        help_text="Год выпуска автомобиля"
    )
    engine_power = models.PositiveIntegerField(
        verbose_name="Мощность двигателя (л.с.)",
        help_text="Мощность двигателя в лошадиных силах"
    )
    drive_type = models.CharField(
        max_length=10, choices=DRIVE_TYPES, verbose_name="Привод"
    )
    engine_type = models.CharField(
        max_length=10, choices=ENGINE_TYPES, verbose_name="Тип двигателя"
    )
    price_per_day = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Цена за день"
    )
    discount_policy = models.ForeignKey(
        "RentalDiscount",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="rental_cars",
        verbose_name="Политика скидок",
    )


    class Meta:
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили"


class Model(models.Model):
    """Класс для модели машины."""

    name = models.CharField(
        max_length=100, verbose_name="Модель машины", blank=True, null=True
    )


    class Meta:
        verbose_name = "Модель машины"
        verbose_name_plural = "Модель машины"

    def __str__(self):
        return self.name


class CarFeature(models.Model):
    """
    Модель характеристик автомобиля. Каждая характеристика может быть привязана к автомобилю и иметь описание.
    """

    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name="features",
        verbose_name="Автомобиль",
    )
    name = models.CharField(
        max_length=255,
        verbose_name="Название характеристики",
        help_text="Название характеристики, например: мощность двигателя, тип коробки передач и т.д."
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание характеристики",
        help_text="Описание характеристики автомобиля (необязательное поле)"
    )

    class Meta:
        verbose_name = "Характеристика автомобиля"
        verbose_name_plural = "Характеристики автомобилей"
        unique_together = ("car", "name")  # Гарантирует, что одна характеристика будет уникальной для каждого автомобиля.

    def __str__(self):
        return f"{self.car} - {self.name}"


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

class CarOption(models.Model):
    """
    Дополнительные опции автомобиля.
    """
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name="options",
        verbose_name="Автомобиль"
    )
    name = models.CharField(
        max_length=100,
        verbose_name="Название опции"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Стоимость опции"
    )

    class Meta:
        verbose_name = "Дополнительная опция"
        verbose_name_plural = "Дополнительные опции"

class CarEquipment(models.Model):
    """
    Комплектация автомобиля.
    """
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name="equipments",
        verbose_name="Автомобиль"
    )
    name = models.CharField(
        max_length=100,
        verbose_name="Название комплектации"
    )

    class Meta:
        verbose_name = "Комплектация"
        verbose_name_plural = "Комплектации"

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
            return self.discount_month / 100
        elif days >= 7:
            return self.discount_week / 100
        return 0 

    def __str__(self):
        return self.name


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

    def calculate_total_price(self):
        """ 
        Рассчитывает общую стоимость аренды с учетом скидок.
        """
        if not self.pickup_datetime or not self.return_datetime:
            return None  # Если даты не заданы, возвращаем None

        duration = self.return_datetime - self.pickup_datetime
        days = max(duration.days, 1)  # Минимально 1 день

        daily_price = self.car.price_per_day
        discount = self.car.discount_policy.get_discount(days) if self.car.discount_policy else 0
        total_price = daily_price * days * (1 - discount)

        return round(total_price, 2)  # Округляем до двух знаков после запятой