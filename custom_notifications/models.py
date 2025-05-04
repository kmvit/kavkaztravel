
from django.db import models
from django.conf import settings
from Kavkaztome import settings
from django.core.exceptions import ValidationError

class Notification(models.Model):
    """Модель уведомления пользователя"""
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        verbose_name='Автор', 
        related_name='notifications_sent',
        help_text='Пользователь, который создал уведомление.'
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        verbose_name='Получатель', 
        related_name='notifications_received',
        help_text='Пользователь, которому отправлено уведомление.'
    )
    message = models.TextField(
        verbose_name='Сообщение', 
        help_text='Текст уведомления, которое получит пользователь.'
    )
    timestamp = models.DateTimeField(
        auto_now_add=True, 
        verbose_name='Время создания',
        help_text='Дата и время создания уведомления.'
    )
    unread = models.BooleanField(
        default=True, 
        verbose_name='Непрочитано',
        help_text='Флаг, показывающий, прочитано ли уведомление получателем.'
    )

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
        ordering = ['-timestamp']  # Сортировка по умолчанию
        

    def __str__(self):
        return f'Уведомление от {self.actor.username} для {self.recipient.username} ({self.timestamp:%Y-%m-%d %H:%M})'

    def clean(self):
        """Валидация перед сохранением"""
        if self.actor == self.recipient:
            raise ValidationError("Пользователь не может отправлять уведомление сам себе")
        if not self.message.strip():
            raise ValidationError("Сообщение уведомления не может быть пустым")

class Message(models.Model):
    """Модель сообщения в чате"""
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name='sent_messages', 
        on_delete=models.CASCADE,
        verbose_name='Отправитель'
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name='received_messages', 
        on_delete=models.CASCADE,
        verbose_name='Получатель'
    )
    text = models.TextField(verbose_name='Текст сообщения')
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата отправки'
    )

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['-created_at']
       
    def __str__(self):
        return f"Сообщение #{self.id} от {self.sender.username} к {self.receiver.username} ({self.created_at:%Y-%m-%d %H:%M})"

    
class NotificationSettings(models.Model):
    """Настройки способов доставки уведомлений"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        related_name='notify_settings', 
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    email = models.BooleanField(
        default=True, 
        verbose_name="Email уведомления",
        help_text="Получать уведомления по электронной почте"
    )
    
    class Meta:
        verbose_name = 'Настройка уведомлений'
        verbose_name_plural = 'Настройки уведомлений'

    def __str__(self):
        return f"Настройки уведомлений для {self.user.username}"
