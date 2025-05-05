from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification, NotificationSettings
from .tasks import send_email_task


@receiver(post_save, sender=Message)
def create_notifications(sender, instance, created, **kwargs):
    """Создает и отправляет уведомление, если пользователь разрешил email-оповещения.

    Логика работы:
    - Уведомление создается всегда при новом сообщении
    - Отправка по email происходит ТОЛЬКО если:
        1. Существует запись NotificationSettings для получателя
        2. Поле email=True в этих настройках
    """
    if not created:
        return

    # Создаем уведомление в любом случае
    notification = Notification.objects.create(
        actor=instance.sender,
        recipient=instance.receiver,
        message=instance.text,
    )

    # Проверяем настройки получателя
    try:
        settings = NotificationSettings.objects.get(user=instance.receiver)
        if settings.email:  # Отправляем только если явно разрешено
            send_email_task.delay(notification.id)

    except NotificationSettings.DoesNotExist:
        # Если настроек нет - не отправляем
        pass
