from celery import shared_task
from django.core.mail import send_mail
from twilio.rest import Client  # Пример для отправки SMS через Twilio
from .models import Notification
from django.conf import settings
import logging


@shared_task
def send_email_task(notification_id):
    try:
        # Получаем уведомление по ID
        print('Получаем уведомление с ID: %s', notification_id)
        notification = Notification.objects.get(id=notification_id)
        print('Найдено уведомление: %s', notification)
        
        # Отправляем email
        send_mail(
            "Новое уведомление",
            notification.message,
            'noreply@yourapp.com',  # Адрес отправителя
            [notification.recipient.email],  # Получатель
        )
        print('Письмо успешно отправлено пользователю %s', notification.recipient.email)
    except Exception as e:
        print('Ошибка при отправке email уведомления: %s', str(e))
