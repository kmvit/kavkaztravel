from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username",)

    USER_TYPE_CHOICES = (("regular", "Regular"), ("owner", "Owner"), ("guide", "Guide"))
    user_type = models.CharField(
        max_length=10, choices=USER_TYPE_CHOICES, default="regular"
    )
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username

# sms/models.py

from django.db import models
import random
import string
from datetime import timedelta
from django.utils import timezone

class SMSVerification(models.Model):
    phone_number = models.CharField(max_length=15)  # Номер телефона получателя
    verification_code = models.CharField(max_length=6)  # Код подтверждения
    message_id = models.CharField(max_length=100, unique=True)  # ID сообщения
    status = models.CharField(max_length=50, default='queued')  # Статус ('queued', 'sent')
    created_at = models.DateTimeField(auto_now_add=True)  # Время отправки
    expires_at = models.DateTimeField()  # Время, до которого код действителен

    def __str__(self):
        return f"Verification for {self.phone_number}, Code: {self.verification_code}"

    def is_expired(self):
        """Проверка, не истек ли срок действия кода."""
        return timezone.now() > self.expires_at
