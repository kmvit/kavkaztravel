from rest_framework import serializers
from .models import Message, NotificationSettings, Notification

class MessageSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели сообщений.
    """
    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'text', 'created_at']
       

class NotificationSettingsSerializer(serializers.ModelSerializer):
    """
    Сериализатор для настроек уведомлений.
    """
    class Meta:
        model = NotificationSettings
        fields = ['email']
        extra_kwargs = {
            'email': {
                'help_text': 'Получать уведомления по электронной почте'
            }
        }

class NotificationSerializer(serializers.ModelSerializer):
    """
    Сериализатор для уведомлений.
    """
    class Meta:
        model = Notification
        fields = ['id', 'actor', 'recipient', 'message', 'timestamp', 'unread']