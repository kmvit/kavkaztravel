from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification, NotificationSettings
from .tasks import send_email_task

@receiver(post_save, sender=Message)
def create_notifications(sender, instance, created, **kwargs):
    print("Процесс пошел.")
    if not created:
        return
    print(1001)
    # Создаем уведомление
    notification = Notification.objects.create(
        actor=instance.sender,
        recipient=instance.receiver,
        message=instance.text,
    )
    print(notification)
    # Получаем настройки уведомлений для получателя
    settings = NotificationSettings.objects.get(user=instance.receiver)
    print(settings)
    # Отправляем уведомления через Celery в зависимости от настроек
    if settings.email:
        send_email_task.delay(notification.id)  # Передаем ID уведомления