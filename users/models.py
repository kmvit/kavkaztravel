from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.validators import validate_phonenumber

class CustomUser(AbstractUser):

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username",)

   # Конкретизация типа владельцев
    USER_TYPE_CHOICES = (
        ("regular", "Regular"),  # Обычный пользователь
        ("restaurant_owner", "Restaurant Owner"),  # Владелец ресторана
        ("hotel_owner", "Hotel Owner"),  # Владелец отеля
        ("carsharing_owner", "Carsharing Owner"),  # Владелец каршеринга
        ("tour_operator", "Tour Operator"),  # Туроператор
        ("guide", "Guide"),  # Гид
    )
    user_type = models.CharField(
        max_length=25, choices=USER_TYPE_CHOICES, default="regular"
    )
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField(
        blank=True,
        validators=[validate_phonenumber],
        verbose_name="Номер телефона",
        help_text="Номер телефона, актуальный формат: +Х XXXXXXXXXX",
    )
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username



class SMSVerification(models.Model):
    """
    Модель для хранения информации о процессе верификации номера телефона через SMS.

    Используется для отслеживания отправки кода подтверждения на номер телефона, 
    а также для управления состоянием верификации и сроком действия кода.
    """
    
    phone_number = models.CharField(max_length=15)  # Номер телефона получателя
    verification_code = models.CharField(max_length=6)  # Код подтверждения
    message_id = models.CharField(max_length=100, unique=True)  # ID сообщения
    status = models.CharField(
        max_length=50, default="queued"
    )  # Статус ('queued', 'sent')
    created_at = models.DateTimeField(auto_now_add=True)  # Время отправки
    expires_at = models.DateTimeField()  # Время, до которого код действителен

    def __str__(self):
        return f"Verification for {self.phone_number}, Code: {self.verification_code}"

    def is_expired(self):
        """Проверка, не истек ли срок действия кода."""
        return timezone.now() > self.expires_at


from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.conf import settings

class Booking(models.Model):
    """
    Модель для бронирования объектов (туров, жилья или кашеринга).
    """
    
    BOOKING_STATUS_CHOICES = (
        ('archived', 'Архив'),
        ('active', 'Активно'),
    )

    PAYMENT_STATUS_CHOICES = (
        ('paid', 'Оплачено'),
        ('unpaid', 'Неоплачено'),
    )
    
    # Список допустимых моделей
    VALID_CONTENT_MODELS = ['tour', 'hotel', 'auto', 'guide']

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="booking", verbose_name="Получатель")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    status = models.CharField(
        max_length=8,  # изменено с 10 на 8
        choices=BOOKING_STATUS_CHOICES,
        default='active',
        verbose_name="Статус брони"
    )
    payment_status = models.CharField(
        max_length=6,  # изменено с 10 на 6
        choices=PAYMENT_STATUS_CHOICES,
        default='unpaid',
        verbose_name="Статус оплаты"
    )
    booking_date = models.DateTimeField(verbose_name="Дата брони")

    # Поля для связи с разными моделями (Generic Relation)
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name="Тип объекта",
        limit_choices_to={
            'model__in': ['tour', 'hotel', 'auto', 'guide']
        }
    )
    object_id = models.PositiveIntegerField(verbose_name="ID объекта")
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        unique_together = ['content_type', 'object_id']

    def __str__(self):
        return f"Бронирование {self.pk} ({self.status})"

    def clean(self):
        # Проверяем, существует ли уже бронирование для того же объекта
        existing_booking = Booking.objects.filter(content_type=self.content_type, object_id=self.object_id).first()
        if existing_booking and existing_booking != self:
            raise ValidationError(f"Для объекта с ID {self.object_id} и типом {self.content_type} уже существует бронирование.")

class Notification(models.Model):
    """
    Модель для хранения уведомлений.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications", verbose_name="Получатель")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="sent_notifications", verbose_name="Отправитель")
    message = models.CharField(max_length=255, verbose_name="Сообщение")
    is_read = models.BooleanField(default=False, verbose_name="Прочитано")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"Уведомление для {self.user.username}: {self.message}"

    class Meta:
        ordering = ['-created_at']
