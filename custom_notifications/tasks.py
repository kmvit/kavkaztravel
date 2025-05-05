from celery import shared_task
from django.core.mail import send_mail
from .models import Notification
from django.conf import settings


@shared_task
def send_email_task(notification_id):
    try:
        # Получаем уведомление по ID
        notification = Notification.objects.get(id=notification_id)

        # Отправляем email
        send_mail(
            "Новое уведомление",
            notification.message,
            [notification.actor.email],  # Адрес отправителя
            [notification.recipient.email],  # Получатель
        )
    except Exception as e:
        print("Ошибка при отправке email уведомления: %s", str(e))
